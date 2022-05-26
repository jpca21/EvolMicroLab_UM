# Natural selection inference via codeml package

#### Author: Mauricio Morales (CGB, Universidad Mayor).

#### Last update: May 26, 2022.

---------------

## 1. Installing PAML and CODEML.

(PAML official page)[http://abacus.gene.ucl.ac.uk/software/paml.html]

In the page above is possible read all the instructions for the installation, if you want to install on your local machine. As a team we are using PAML on a HCP system (due to the size of the files to analyzes). 

There is a GUI and a terminal version. We recommend that you use the terminal version. 

Some recommendations from PAML:
>A number of example datasets are included in the package. They are typically datasets analyzed in the original papers that described the methods. I suggest that you get a copy of the paper, and run the example datasets to reproduce our results first, before analyzing your own data. This should serve to identify errors in the program, help you to get familiar with the format of the data file and the interpertation of results.

## 2. Data needed.

* Fasta files of nucleotide and amino acids of protein of interest (both files must to have the same headers).
* Tree file that contain the information about all the secuences. 

## 3. Process summary.

* Identified homologs.
* Build multiple sequence alignment (MSA).
* Quality control of MSA.
* Phylogeny inferences.
* Estimates of the effect of natural selection on protein-coding.

## 4. Get the sequences files.

* Download genomes from the corresponding database, for example, NCBI.
* Use python or perl (or some other available program) to extract the coding sequences of interest.
* Once the sequence is obtained, make sure you have the sequences in fasta format, both in nucleotides and amino acids.
* Proceed to generate the sequences in codon format, using the PAL2NAL program (PAL2NAL official page)[http://www.bork.embl.de/pal2nal/], which takes the amino acid and nucleotide sequences to obtain the codons.

## 5. Use IQ-Tree to estimate the phylogeny.

* Estimate the phylogeny. A recommended program is IQ-tree (IQ-Tree official page)[http://www.iqtree.org/]. For more information about the program, visit the manual on the official page. 
* Using the sequences in nucleotides, it´s neccessary to proceed with the MSA, we recommend use MAFFT or ClustaW. IQ-Tree accept Fasta or Phylip formats. 
* If you need more information about the MSA, visit the official page of your selected MSA (MAFFT official page)[https://mafft.cbrc.jp/alignment/server/]. In this case, you need to use the sequences in nucleotides. 
* After the MSA, you need to use the MSA quality control. There are some programs that could help you, your selection depends on your goal (phylogeny inference, postraductional modifications, etc.).
* To estimate the phylogeny it is necessary to find and select the substitution model that best fits the data. For this, in the first analysis it is necessary to use ModelFinder (included in IQ-Tree).
* Once the best model has been found, it is necessary to return to the analysis but this time select the model selected.
* To add support for branch and node length estimation, it is necessary to use a non-parametric test. IQ-tree has UFBoot (analysis for bootstrap support). Depending on the size of the data (number of sequences) you can choose between 100-1,000-10,000 bootstrap.
* If more analyzes are necessary for the estimation of the phylogeny, all depends on your goal. Phylogeny estimation delivers a set of files, which includes the phylogenetic tree.

## 6. Omega (dN/dS) estimation.

* Use CODEML package to estimate natural selection. Creates a text file (codeml.ctl) with contain the specific instructions of each parameters used for the program. Here an example of this file: 
```
seqfile = Ceacam_seq.txt * sequence data filename
treefile = Ceacam_tree.txt * tree structure file name
outfile = Ceacam_ModelA.out * main result file name
seqtype = 1 * 1:codons; 2:AAs; 3:codons-->AAs
model = 2 * models for codons ...
NSsites = 2 * 0:one w;1:neutral;2:selection ...
cleandata = 1 * remove sites with ambiguity ...
```
* IMPORTANT: the combiantions of parameters depends of your goal, so there are more parameters avalaible. Search in literature for more detail. 
* There are some codon models to estimate natural selection, depending on your goal, select the best for your data based on literature. 
* 
