# OrthoFinder related worflows

The latest official release, **OrthoFinder v2.5.4**, has a couple of bugs. The first is already solved, see it here:

<https://github.com/davidemms/OrthoFinder/issues/602>

To get the code which fixes this bug

```
git clone https://github.com/davidemms/OrthoFinder
```

Then use that executable. If you download the tarball from the latest release or use conda with the latest release, you won't get the latest additions to the code, **which aren't released yet**.


The second relevant bug is reported here (includes the solution), and affects `tools/create_files_for_hogs.py` :

<https://github.com/davidemms/OrthoFinder/issues/647>

### `orthofinder_hogs_from_clades.job`

This script generates single-copy HOGs from a list of nodes. These nodes
have to be selected from the species tree generated after running `orthofinder -ft -s tree_file` (see `Workflows/OrthoFinder/orthofinder_HOGs_worflow.md`).
**Check the results in `single_copy_HOGs/` and `HOGs_seqs/` inside `/mnt/DATA/jmaturana/OrthoFinder/Results_Nov25/HOGs_seqs` `@coyhaique`**