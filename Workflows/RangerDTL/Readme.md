# 1. Ranger-DTL pipeline

For general info about `Ranger-DTL`  see:

<https://compbio.engr.uconn.edu/software/ranger-dtl/>

**For a sbatch example, check `Workflows/RangerDTL/ranger_dtl.job`**

`Ranger-DTL` needs a species tree and gene trees. It  accepts rooted or un-rooted trees, 
but the default pipeline works with rooted trees. OrthoFinder produces rooted species and
gene trees and those will be used.

## 1.1. `edit_species_tree.py`

Because `ranger` complains about the format of the leaves' labels (assemblies names)
and fails, we need to edit/convert all these names in the species (only one) and gene trees (multiple trees).

```sh
# For help
python edit_species_tree.py -h
python edit_species_tree.py SpeciesTree_rooted_node_labels.txt /output/dir
```
The output of this step, an edited tree and a `pkl` file,  will be used with `ranger-dtl_pipeline.py`


## 1.2. Select trees for each single-copy OG ("scogs")

Given that OrthoFinder doesn't produce trees for HOGs but for OGs, we'll use the OGs from `Single_Copy_Orthologue_Sequences` to
obtain a list of OGs. With this list, we'll select the gene trees from `Resolved_Gene_Trees/` (inside the OrthoFinder results directory).


```sh
# Go to the orthofinder results directory
cd Results_{date}
mkdir single_copy_trees
parallel  "cp Resolved_Gene_Trees/{/.}_tree.txt single_copy_trees" ::: Single_Copy_Orthologue_Sequences/*
```

`Single_Copy_Orthologue_Sequences/*` expands to all the files in that folder and  `{/.}` prints `${og_name}`, for example `OG0000331`.

## 1.3. Run the pipeline

`ranger-dtl_pipeline.py` runs `Ranger-DTL.linux` and `AggregateRanger.linux` .
You may pass the path to those binaries  (included within the source of the program). If you already
have those in your path, this isn't needed. Also, we have to pass the modified species tree and the dictionary (`.pkl` 
file) from the `edit_species_tree.py` step, and the input trees from the previous step (`single_copy_trees/`).

From the `Ranger-dtl_Linux`'s manual pdf:

>If there is uncertainty about the event cost assignments to
be used, then we recommend using Ranger-DTL multiple times with a few different event cost
assignments (for instance, 100 samples each using [D, T, L] costs of [2,3,1], [3,3,1], and [2,4,1],
for a total of 300 samples), and then aggregate all samples using AggregateRanger.

The script includes those weights in:

```python
# This is zipped afterwards so doesn't read "like a human"
D,T,L = [2,3,2],[3,3,4],[1,1,1]
```

The script will create ( 3 combinations of weigths * the number of seeds) plus one `pkl` file per tree. After that,
it will run `AggregateRanger.linux` to aggregate those results (one file per tree). Those files will be placed
inside "${output_dir}/AggregateRanger" (see below)

**`-n_seeds 3` is only ok for testing. Change it to  `100`-`500` for an "official" run and use
16+ cores. For a couple hundreds of HOGs and 200 species it should run in 2 hours or less for 200-300 seeds. It's important to use `gnu parallel` 
to run this script because one is iterating hundreds of times over 100+ single-copy gene trees**

We pick a few HOGs to test this pipeline:

 ```sh
unzip ranger_workflow.zip
cd ranger_workflow

# Inputs
sp_tree="Species_Tree/SpeciesTree_rooted_node_labels.txt"

python edit_species_tree.py -h
python edit_species_tree.py SpeciesTree_rooted_node_labels.txt Species_Tree/

edited_stree="Species_Tree/species_tree_edited_rand_N0.nwk"
sname_dict="Species_Tree/sname_to_rand.pkl"
input_trees="single_copy_trees"
# This folder will be created by the script if it doesn't exist. Better if it doesn't exist (or empty)
output_dir="RangerDTL_test"
# number of cores, change it according to your system resources
n_cores=12
# change the n_seeds for and official run
n_seeds=3
# See the help
python ranger-dtl_pipeline.py -h
## Remember to use the proper path for the python script ##
parallel -j $n_cores "python ranger-dtl_pipeline.py $edited_stree \
 {} $sname_dict $n_seeds ${output_dir} -ranger_bin $ranger -aggregate_bin $aggregate" ::: ${input_trees}/*.txt

##See the results in "${output_dir}/AggregateRanger"##

# AggregateRanger folder is hardcoded into ranger-dtl_pipeline.py so don't change it
aggregated_dir="${output_dir}/AggregateRanger"

# Takes all the aggregated files and creates a single summary table.
# The table is named nodes_events.tsv
python aggregate_aggs.py -h
python aggregate_aggs.py $aggregated_dir $sname_dict $n_seeds
```

**Look for `nodes_events.tsv` in `ranger_workflow/RangerDTL_test` **

## Dependencies

python (`>=3.6`) libraries:

- `ete3 >= 3.1.2`

others:

- `orthofinder >= 2.5`
- `gnu parallel >= 2021`