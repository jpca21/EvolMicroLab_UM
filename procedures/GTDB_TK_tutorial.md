# Installing and Using GTDB-TK

#### Author: Damariz Gonzalez (CGB, _UMayor_)

##### last update: May 19, 2022
------------------------------------------------------------------

## 1. Installing Miniconda3

The first step is to make sure that we have conda installed in our device, the developers of GTDBTK recommend to use [miniconda3](https://docs.conda.io/en/latest/miniconda.html). The programm is a bit tricky in its installation so, make sure that you are using miniconda3. If you don't have miniconda installed, you can type in your Linux or Mac terminal:

		wget "LINK TO YOUR PACKAGE"  

You can find the link to your miniconda packages in the web page, make sure that you are choosing the right one, according with your operative system: https://docs.conda.io/en/latest/miniconda.html.

After the download, execute the file, make sure to put the right name of the package:

		bash Miniconda3.sh

------------------------------------------------------------------

## 2. Install GTDB-TK

To  install gtdbtk run de next command on your terminal:

		conda create -n gtdbtk-1.3.0 -c conda-forge -c bioconda gtdbtk=1.3.0

We are goig to use the 1.3.0 version because the tutorial of de developers is build for this `gtdbtk` folders version configuration. Note that also, it is a posibbility that your enviroment information will be stored in a folder named `.conda` and not in `miniconda3` folder.

------------------------------------------------------------------

## 3. Get reference data

For our gtdbtk version we are going to download a specific reference data release. This is release95. Just type the next command on your terminal:

	wget https://data.ace.uq.edu.au/public/gtdb/data/releases/release95/95.0/auxillary_files/gtdbtk_r95_data.tar.gz

**Warning**: Note that the file is pretty heavy, so use a slurm/nohup script to make things faster and increase the cpus for the task is a good option.(recommended)

------------------------------------------------------------------

## 4.Configure Paths

We are going to give the path of reference data downloaded in the previous step to the gtdbtk executable:

 		eco "export GTDBTK_DATA_PATH=path/to/release/package" \ > /miniconda3/envs/gtdbtk-1.3.0/etc/conda/activate.d/gtdbtk.sh
 
**Note that** maybe you have the information in your `.conda` folder instead of `miniconda3`. So just replace the "miniconda" by ".conda".

Now we are going to activate the enviroment:

		conda activate gtdbtk-1.3.0

And check if everything is working just fine!:

		gtdbtk --h

If there is no error, it is time to run gtdbtk.

------------------------------------------------------------------

## 5. Prepare the folders

		mkdir dir_name
		cd dir_name
		mkdir genomes

Now you have to place your .fna or .fna.gz data set on the `genomes` folder.

Place yourself one folder out of your `dir_name` folder.

------------------------------------------------------------------

## 6. Identify

First we do the gene calling:

		gtdbtk identify --genome_dir dir_name/genomes --out_dir dir_name/identify

**Note**: you can add also the amount of cpus you want to use with `--cpus`(recommended)
**Note**: you can add also the format of the file id you are using gz files with `--extension gz`

------------------------------------------------------------------

## 7. Align

Next step is aligning the genomes:

		gtdbtk align --identify_dir dir_name/identify/ --out_dir dir_name/align 

**Note**: Here you can also add the `--cpus` amount.(recommended)

------------------------------------------------------------------

## 8. Classify

    gtdbtk classify --genome-dir dir_name/genomes --align_dir dir_name/align --out_dir dir_name/classify

**Note**: you can add also the amount of cpus you want to use with `--cpus` (recommended) 
**Note**: You can specify if you are using gz files with `--x gz`.
