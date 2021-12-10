#! /usr/bin/env bash

# GNU parallel required, present in most of the linux systems, compatible with mac osx too
# Run it:
# bash Align_single-copy_genes.sh results_Nov20/Single_Copy_Orthologue_Sequences Results_Nov20/alignments 12

# Align all the genes from the single-copy orthogroups produced by `orthofinder`
# First argument: The directory `Single_Copy_Orthologue_Sequences` from orthofinder.
# Second argument: The folder where you want to place the alignment files.
# Third argument: Number of proccesses run in parallel. ex: 4

# Pass **all the paths without trailing '/'**, they can be absolute or relative. Example:
# fasta_dir='relative/Results_Nov09/Single_Copy_Orthologue_Sequences'
# fasta_dir='/absolute/Results_Nov09/Single_Copy_Orthologue_Sequences'

fasta_dir=$1
align_dir=$2
# number of proccesses run in parallel, each process will use 1 core by default, 
# because short aligments. 
n_cores=$3


mkdir -p "$align_dir"
parallel -j $n_cores --plus "mafft --thread 1 --maxiterate 1000 --localpair {} > \
$align_dir/{/.}.fa 2>> $align_dir/mafft.log" ::: $fasta_dir/*.fa


# The same, sequential, for the terminal (without user input):
## for fasta in *.fa; do name=$(basename $fasta .fa); mafft --maxiterate 1000 --globalpair
##                        --clustalout $fasta > "alignments/${name}.aln" 2> /dev/null; done


#Trim all the columns composed of 100% gaps. These alignments should be concantenated afterwards
# parallel -j $n_cores --plus "trimal -in  $align_dir/{/.}.fa -out $align_dir/{/.}_trimal.fa  -noallgaps \
# -fasta -sgc > $align_dir/{/.}_trimal.scores" ::: $fasta_dir/*.fa
