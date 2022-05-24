# Natural selection inference via codeml package

#### Author: Mauricio Morales (CGB, Universidad Mayor).

#### Last update: May 24, 2022.

---------------

1. Installing PAML and CODEML.

(PAML official page)[http://abacus.gene.ucl.ac.uk/software/paml.html]

In the page above is possible read all the instructions for the installation, if you want to install on your local machine. As a team we are using PAML on a HCP system (due to the size of the files to analyzes). 

There is a GUI and a terminal version. We recommend that you use the terminal version. 

Some recommendations from PAML:
>A number of example datasets are included in the package. They are typically datasets analyzed in the original papers that described the methods. I suggest that you get a copy of the paper, and run the example datasets to reproduce our results first, before analyzing your own data. This should serve to identify errors in the program, help you to get familiar with the format of the data file and the interpertation of results.

2. Data needed.

* Fasta files of nucleotide and amino acids of protein of interest (both files must to have the same headers).
* Tree file that contain the information about all the secuences. 

3. Process summary.

* Identified homologs.
* Build multiple sequence alignment (MSA).
* Quality control of MSA.
* Phylogeny inferences.
* Estimates of the effect of natural selection on protein-coding.

4. Get the sequences data.

