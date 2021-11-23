# OrthoFinder related worflows

- `orthofinder_hogs_from_clades.job` generates single-copy HOGs from a list of nodes. These nodes
have to be selected from the species tree generated after running `orthofinder -ft -s tree_file` (see `orthofinder_HOGs_worflow.md`). The idea is to select nodes that have as children groups of genomes classified as the same species. These can be done using 
parsed trees with the gtdb species classification as the tips/leaves labels. See `Trees_ete3/ete3_tree_parsing.ipynb` as an example of parsing.

**wip**