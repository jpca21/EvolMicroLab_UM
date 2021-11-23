# OrthoFinder related worflows

The latest official release, **OrthoFinder v2.5.4**, has a couple of bugs. The first is already solved, see it here:

<https://github.com/davidemms/OrthoFinder/issues/602>

To get the code which fixes this bug, do a 

```
git clone https://github.com/davidemms/OrthoFinder
```
Thay will download the latest code. If you download the tarball from the latest release, you won't get the latest additions to the code, which aren't released yet.


The second relevant bug is reported here (includes the solution), and affects `tools/create_files_for_hogs.py` :

<https://github.com/davidemms/OrthoFinder/issues/647>

## `orthofinder_hogs_from_clades.job`

This script generates single-copy HOGs from a list of nodes. These nodes
have to be selected from the species tree generated after running `orthofinder -ft -s tree_file` (see `orthofinder_HOGs_worflow.md`). The idea is to select nodes that have as children groups of genomes classified as the same species. These can be done using 
parsed trees with the gtdb species classification as the tips/leaves labels. See `Trees_ete3/ete3_tree_parsing.ipynb` as an example of parsing.

**wip**

Add information about the orthofinder runs and their locations in coyhaique