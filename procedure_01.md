# Cleaning reads using Cutadapt

This document is a brief demonstration about the use of [Cutadapt](https://github.com/marcelm/cutadapt) in the `Coyhaique` server.

## Install cutadapt, fastqc and multiqc in a conda environment

```conda create -n cutadapt cutadapt fastqc multiqc```

```conda activate cutadapt```

## Making QC for raw Illumina reads 

Assuming all your files are in the same folder, and they can be traced using `*sequence.fastq`, execute the following commands:

```
mkdir QCraw
fastqc *sequence.fastq -o QCraw -t 50
multiqc ./QCraw/* -o QCraw
```

Consult the `multiqc_report.html` file generated in the `QCraw` folder

## Execute Cutadapt 

Consider that in this example you are working with nextera data. Therefore, the adapters you need to remove are the following:

```
>PrefixNX/1
AGATGTGTATAAGAGACAG
>PrefixNX/2
AGATGTGTATAAGAGACAG
>Trans1
TCGTCGGCAGCGTCAGATGTGTATAAGAGACAG
>Trans1_rc
CTGTCTCTTATACACATCTGACGCTGCCGACGA
>Trans2
GTCTCGTGGGCTCGGAGATGTGTATAAGAGACAG
>Trans2_rc
CTGTCTCTTATACACATCTCCGAGCCCACGAGAC
```

Consider the helpful information from `cutadapt --help`, or consult the [documentation here](https://cutadapt.readthedocs.io/en/stable/index.html). Execute the following `cutadapt` command:

```
for aa in `dir -1 *.fastq | cut -d "_" -f1,2 | sort | uniq` ; do echo $aa;   \
cutadapt --cores 40 -u 15 -U 15 -q 20 -Q 20 --max-n 0 -m 80 \
 -b TCGTCGGCAGCGTCAGATGTGTATAAGAGACAG -B CTGTCTCTTATACACATCTGACGCTGCCGACGA  \
 -B TCGTCGGCAGCGTCAGATGTGTATAAGAGACAG -b CTGTCTCTTATACACATCTGACGCTGCCGACGA  \
 -b GTCTCGTGGGCTCGGAGATGTGTATAAGAGACAG -B CTGTCTCTTATACACATCTCCGAGCCCACGAGAC \
 -B GTCTCGTGGGCTCGGAGATGTGTATAAGAGACAG -b CTGTCTCTTATACACATCTCCGAGCCCACGAGAC \
 -b AGATGTGTATAAGAGACAG -B AGATGTGTATAAGAGACAG \
 --pair-filter=any -o $aa\_1_trimmed.fastq -p $aa\_2_trimmed.fastq  \
 $aa\_1_sequence.fastq $aa\_2_sequence.fastq > $aa\_report.txt ;  \
done
```

## QC for the trimmed reads

```
mkdir QCtrimmed
fastqc *trimmed.fastq -o QCtrimmed -t 50
multiqc ./QCtrimmed/* -o QCtrimmed
```

```conda deactivate```

Consult the `multiqc_report.html` file generated in the `QCtrimmed` folder
