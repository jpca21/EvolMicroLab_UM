#!/bin/bash -l

## Cluster hypothetical proteins to avoid running long searches with hmmer and others ##
## This reduced the amount of sequences about 10 times ##

root="root/for/this/project/Clustering"
db_dir="${root}/mmseq_akk_hypo_db"
fasta="your/multifasta/hypothetical_proteins.fa"
db_name="akk_hypo"

cd $root

mkdir $db_dir
mmseqs createdb $fasta $db_dir/$db_name

clusters_dir="mmseqs_cluster90_70"
clusters_name="akk_hypo_clu"

# Clustering by 90% mutual coverage, 70% identity
mkdir $clusters_dir
min_seq_id=0.7
mmseqs cluster $db_dir/$db_name $clusters_dir/$clusters_name tmp --cov-mode 0 -c 0.9 \
 --min-seq-id $min_seq_id --threads 8
 
# Create a "sub-db" and get the representative sequences in fasta format

sub_clusters_dir="mmseqs_cluster90_70_sub"
sub_clusters_name="akk_hypo_clu_rep"

mkdir $sub_clusters_dir

mmseqs createsubdb $clusters_dir/$clusters_name $db_dir/$db_name \
 $sub_clusters_dir/$sub_clusters_name

# Representative sequences
rep_fasta="akk_hyp_clu90_70_rep.fasta"
 
mmseqs convert2fasta $sub_clusters_dir/$sub_clusters_name $rep_fasta

# Get the mappings between cluster representatives and members
cluster_tsv="akk_annot_clu.tsv"
mmseqs createtsv $db_dir/$db_name $db_dir/$db_name $clusters_dir/$clusters_name $cluster_tsv

echo **How many sequences are in the original fasta and in the representatives fasta?**

rg -c '^>' $fasta
rg -c '^>' $rep_fasta

