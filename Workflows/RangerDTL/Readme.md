# 1. Ranger-DTL pipeline

For general info abour `Ranger-DTL`  see:

<https://compbio.engr.uconn.edu/software/ranger-dtl/>

`Ranger-DTL` needs a species tree and gene trees. It  accepts rooted or un-rooted trees, 
but the default pipeline works with rooted trees. OrthoFinder produces rooted species and
gene trees and those will be used.

## 1.1. `edit_species_tree.py`

Because `ranger` complains about the format of the leaves' labels (assemblies names)
and fails, we need to edit/convert all these names in the species (only one) and gene trees (multiple).

```sh
# For help
python edit_species_tree.py -h
python edit_species_tree.py SpeciesTree_rooted_node_labels.txt /output/dir
```
The output of this step, an edited tree and a `pkl` file,  will be used with `ranger-dtl_pipeline.py`

## 1.2. Select trees for each single-copy HOG ("scogs")

As rooted gene trees, we'll use the single-copy resolved gene trees from `Resolved_Gene_Trees/` 
inside the OrthoFinder results directory. We create a list of single-copy OGs "scogs":

```sh
# See the help first:
python single_copy_hogs.py -h
python single_copy_hogs.py /Phylogenetic_Hierarchical_Orthogroups N50  N50/HOG_Sequences Species_Tree/SpeciesTree_rooted_node_labels.txt /output/dir
# This produces as output 'single_copy_HOGs_N50.list'
# copy the trees for each scog using gnu parallel or any other method:
mkdir -p scogs_n50_trees
parallel  "cp ../Resolved_Gene_Trees/{}_tree.txt scogs_n50_trees" :::: single_copy_HOGs_N50.list
```

 `../Resolved_Gene_Trees/` is the path to (all) the trees. Parallel will place the name of the HOG in place of the  `{}`.

## 1.3. Run the pipeline

`ranger-dtl_pipeline.py` includes most of the steps to run  `Ranger-DTL.linux` and `AggregateRanger.linux` .
You may pass the path to those binaries  (included within the source of the program). If you already
have those in your path, this isn't needed. Also, we have to pass the modified species tree and the dictionary (`.pkl` 
file) from the `edit_species_tree.py` step, and the input trees from the previous step ("scogs" trees).

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
16+ cores. For many hundreds of HOGs it should run in 2-3 hours or less. It's important to use `gnu parallel` to run this script because usually one is iterating through hundreds of HOGs**

We pick a few HOGs to test this pipeline:

 ```sh
unzip ranger_workflow.zip
cd ranger_workflow

# Inputs
edited_stree="species_tree_edited_rand_N0.nwk"
sname_dict="sname_to_rand.pkl"
input_trees="scogs_test_trees"
# This will be created by the script if it doesn't exist. Better to be an empty folder
output_dir="RangerDTL_test"
# number of cores, change it according to your system resources
n_cores=12
# n_seeds=3
# See the help
python ranger-dtl_pipeline.py -h
## Remember to use the proper path for the python script ##
parallel -j $n_cores "python ranger-dtl_pipeline.py $edited_stree \
 {} $sname_dict $n_seeds ${output_dir} -ranger_bin $ranger -aggregate_bin $aggregate" ::: ${input_trees}/*.txt

##See the results in "${output_dir}/AggregateRanger"##

# AggregateRanger is hardcoded into ranger-dtl_pipeline.py so don't change it
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