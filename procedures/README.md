# Procedures in Coyhaique

## Installing and using `metawrap` in your session 

The [metaWRAP package](https://github.com/bxlab/metaWRAP) is a customizable pipeline for binning and bin refinement, with powerful applications in the generation of MAGs (_metagenome-assembled genomes_). The recommended metaWRAP installation uses a combination of preconfigured executables and a supporting _conda_ environment. To properly function, you must install and activate the conda environment and define the executable in the PATH. 

In `Coyhaique`, the executables and databases are already present in the folders `/mnt/DATA/metaWRAP/bin` and `/mnt/DATA/metaWRAP/DBs` respectively.

From the original metawrap environment, I created a custom environment list to facilitate its installation (metawrap_custom_list.yml). To use this file for the installation of the environment, use the following command:

```
conda create --name metawrap --file metawrap_custom_list.yml
``` 

To include the metawrap `bin` folder in the `PATH`, put this instruction in the `.bashrc` file of your session:

```
# User specific environment (MetaWRAP)
if [ -d "/mnt/DATA/metaWRAP/bin" ]
then
    PATH="/mnt/DATA/metaWRAP/bin:$PATH"
fi
export PATH
```

With those changes, you can then activate the `metawrap` environment:

```
conda activate metawrap
```

And then using in from the bin folder.
