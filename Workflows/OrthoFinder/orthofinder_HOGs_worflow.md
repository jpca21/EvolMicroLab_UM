# Hierarchical OGs pipeline

The new OrthoFinder pipeline defines Hierarchical OGs (HOGs) using the
rooted gene trees instead of the gene graph approach (MCL like). According to the author, this is 12% more accurate that the previous OrthoFinder and other software.
The first step is to run OrthoFinder as always. I use the `msa`  option because can get you a more accurate species tree/results, but it isn't mandatory :

```sh
orthofinder.py -f $faas -M msa -y -t 28 -a 8
```

Then, checking the species trees from `Species_Tree/SpeciesTree_rooted_node_labels.txt`,
we have to see if the proper outgroup was selected (this is important for accuracy).
Usually, OrthoFinder doesn't select the proper outgroup, but inside `Species_Tree/Potential_Rooted_Species_Trees`
creates alternative trees with different outgroups. Pick from there the proper species tree and run OrthoFinder again, but only the last steps, "from trees" `-ft`:

```sh
orthofinder.py -ft ${previous_results} -s "${previous_results}/${rooted_tree}" -y -t 28
```

where `$previous_results` is the previous output's directory and `rooted_tree` is the
selected tree with the proper outgroup. This run takes a small fraction of the original run's time, because all the comparisons between sequences are already done. The result from this run wil be used from now on.
Once this is done, we can create the HOGs sequences from a specific hierarchical level,
which is the node name in `Species_Tree/SpeciesTree_rooted_node_labels.txt`. This is
done by using `create_files_for_hogs.py` included within the OrthoFinder source code.

```sh
# See the help with -h
python OrthoFinder/tools/create_files_for_hogs.py  OrthoFinder/${output_dir} \
${output_dir}/${hogs_dir} N1
 ```

 This will create all the HOGs sequence files for the node N1 but we could select any node.
 **The N1 node has the particularity that should include all the genomes except the outgroup**.
 We'll pass this directory to the next step, to select single copy HOGs present in all these genomes.

To do that we need the file that describes all the OGs present in any particular level, which are in `Phylogenetic_Hierarchical_Orthogroups/`,
the HOGs sequences created by `create_files_for_hogs.py` and the species tree. From there, we can run :

```sh
python single_copy_hogs.py -h
# This produces as output 'single_copy_HOGs_N1.list'
python single_copy_hogs.py Phylogenetic_Hierarchical_Orthogroups/ N1  N1/HOG_Sequences Species_Tree/SpeciesTree_rooted_node_labels.txt
# copy the sequence for each hog using gnu parallel or any other method:
mkdir -p scogs_N1_seqs
parallel  "cp OrthoFinder/${output_dir}/N1.H{}.fa scogs_N1_seqs" :::: single_copy_HOGs_N1.list
 ```

 `N1.{}.fa` is the file name of the sequences. `parallel` will replace the `{}` with the OG
name from the list. `OrthoFinder/${output_dir}` is the output folder used with `create_files_for_hogs`.

### About the N selected

If we select the N0 as node for `create_files_for_hogs.py`, we'll have all the HOGs, which include also all the HOGs for N1, N2, N3 and so on. The important thing is when using `single_copy_hogs.py`, we pass the proper N. So
if we created the hogs files for N0, then we still can use:

```sh
python  single_copy_hogs.py Phylogenetic_Hierarchical_Orthogroups/ N1  N0/HOG_Sequences Species_Tree/SpeciesTree_rooted_node_labels.txt
```

## Dependencies

python (`>=3.6`) libraries:

- `ete3 >= 3.1.2`
- `pandas >= 1.1`

others:
- `orthofinder >= 2.5`
- `gnu parallel >= 2021`
