# EvolMicroLab_UM
This repostory is the Main Group Repository. 

## More links

##### More info [about the team here](https://github.com/jpca21/EvolMicroLab_UM/blob/main/About_our_lab.md)
##### Procedure: [using cutadapt in Coyhaique](https://github.com/jpca21/EvolMicroLab_UM/blob/main/procedure_01.md)


# About our server
## How to run jobs in the group computer, "coyhaique"

Once a user is logged-in in the cluster, any command and/or script can be run as in your local computer. 
The key here are the r-w-x permissions for each user.

When executing any script/command (job) in the terminal, is always recommended to append 
`nohup`. For example:

```
$ nohup bash my_script.sh &
$ nohup python my_code.py &
```

This will allow the program to keep running even when the terminal gets closed (unintentionally 
or not). The `&` is not needed, but it's useful because sends the process to the 
background, so one can continue to use the same terminal without having to wait for the 
command to finish.

## Resources

Cores: 32
Memory: 128 GB
Sytem disk: 500 GB SSD
Storage: 16TB raid 1+0 (10)

The computer has 32 cores and each core has 2 threads. `lscpu` reports
64 cpus, but that is the number of threads. 32 is the important number here. When 
running a job, it is the user responsability to know how many cores will be 
used by it. It is always possible to run `top`/`htop` to see how many cpus are being used.

The maximum amount of resources for each job depends on the particular circumstances, but it is
sensible to use no more than half of the resources if multiple users will be running jobs. This is
not a personal computer and users should always remember that.

## Storage

### Big disk (16 TB)

Each user has to make a directory in `/mnt/DATA/` named after its user name, which will 
be used as its personal folder. Users has to place all/most of their files here.

### Databases

Most of the time, databases should be shared among users. Databases are only read (programs don't modify them) 
and frequently weight at least a few GBs. Databases should be placed in `/mnt/DATA/DBs`. In this folder, all the 
users have read and writting permissions.

### System disk - SSD

This is mainly for software installation (only 500 GB)

- This disk has the operating system installed in it. All the the software installed by `dnf`/`yum` is placed in `/usr/bin/`. 
- Inside `/home/{user-name}`, the users may install personal software. For example, users can
install anaconda and all its environments here.

Use `df -h` to see the storage use
Use `du -sh /dir/path` to see the size of a directory

## Anaconda

<https://docs.anaconda.com/anaconda/install/index.html>

Users may install most of the software using the `conda` software management, which is installed once the anaconda/miniconda software 
distribution is installed. It isn't mandatory to use the `/home/{user-name}` for the anaconda installation and users can always install 
it inside `/mnt/DATA/{user-name}`. 

After installing anaconda, users will need to set up the bioconda repository:

<https://bioconda.github.io/user/install.html>

About `conda`:

<https://docs.conda.io/projects/conda/en/latest/user-guide/index.html>

`conda` can frequently take several minutes to solve software dependencies. `mamba` is a faster alternative, which is compatible
with `conda`. 

check <https://github.com/mamba-org/mamba>

