# Hierarchical OGs pipeline

The new orthofinder pipeline defines Hierarchical OGs (HOGs) using the
rooted gene trees instead of the gene graph approach (MCL like). According to the author, this is 12% more accurate that the previous orthofinder and other software.
The first step is to run orthofinder as always. I use the `msa` option but it isn't mandatory:

```sh
orthofinder.py -f $faas -M msa -y -t 28 -a 8
```

Then, checking the species trees from `Species_Tree/SpeciesTree_rooted_node_labels.txt`,
we have to see if the proper outgroup was selected (this is important for accuracy).
Usually, orthofinder doesn't select the proper outgroup, but inside `Species_Tree/Potential_Rooted_Species_Trees`
creates alternative trees with different outgroups. We have to pick from there the proper species tree and run orthofinder again, but only the last steps, "from trees" `-ft`:

```sh
orthofinder.py -ft ${previous_results} -s "${previous_results}/${rooted_tree}" -y -t 28
```

where `$previous_results` is the previous output's directory and `rooted_tree` is the
selected tree with the proper outgroup. This run takes a small fraction of the original run, because all the comparisons between sequences are already done. This creates the
tree `SpeciesTree_rooted_node_labels.txt`, which is the same tree we picked in the previous step and we will use in the future.

Once this is done, we can create the HOGs sequences from a specific hierarchical level,
which is the node name in `Species_Tree/SpeciesTree_rooted_node_labels.txt`. This is
done by using `create_files_for_hogs.py` included within the OrthoFinder source code.

```sh
# See the help with -h
python OrthoFinder/tools/create_files_for_hogs.py  OrthoFinder/${output_dir} \
${output_dir}/${hogs_dir} N50
 ```

 This will create all the HOGs sequence files for the node N50. We can select any particular node. We'll pass this directory to the next step, to select single copy HOGs present
 in all the genomes

To do that we need the file that describes all the OGs present in any particular level, which are in `Phylogenetic_Hierarchical_Orthogroups/`,
the HOGs sequences created by `create_files_for_hogs.py` and the species tree. From there, we can run :

```sh
python single_copy_hogs.py -h
# This produces as output 'single_copy_HOGs_N50.list'
python single_copy_hogs.py Phylogenetic_Hierarchical_Orthogroups/ N50  N50/HOG_Sequences Species_Tree/SpeciesTree_rooted_node_labels.txt /output/dir
# copy the sequence for each hog using gnu parallel or any other method:
mkdir -p scogs_n50_seqs
parallel  "cp OrthoFinder/${output_dir}/N50.{}.fa scogs_n50_seqs" :::: single_copy_HOGs_N50.list
 ```

 `N50.{}.fa` is the file name of the sequences. `parallel` will replace the `{}` with the OG
name from the list. `OrthoFinder/${output_dir}` is the output folder used with `create_files_for_hogs`.

## Dependencies

python (`>=3.6`) libraries:

- `ete3 >= 3.1.2`
- `pandas >= 1.1`

others:
`orthofinder >= 2.5`
`gnu parallel >= 2021`
