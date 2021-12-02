# Annotating hypothetical proteins

When annotating the set of 201 akkermansia genomes with prokka, more than 50% of the predicted genes were annotated as *hypothetical proteins* (**263307 of 472481**).


## About `pfam-N`

https://xfam.wordpress.com/2021/03/24/google-research-team-bring-deep-learning-to-pfam/


### 1. Download `Pfam-N.gz` aligment from Pfam ftp.

Pfam-A 35 was recently released but Pfam-N haven't been updated yet.

http://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam34.0/

### 2.  Prepare a profile database for `hmmscan` with `hmmpress`

```sh
$ hmmpress pfam_N.hmm 
Working...    done.
Pressed and indexed 11438 HMMs (11438 names and 11438 accessions).
Models pressed into binary file:   pfam_N.hmm.h3m
SSI index for binary model file:   pfam_N.hmm.h3i
Profiles (MSV part) pressed into:  pfam_N.hmm.h3f
Profiles (remainder) pressed into: pfam_N.hmm.h3p
```

One can use this profile with 3rd party software like  `prokka` and `eggnog-mapper`

### 3. `prokka`

`prokka` doesn't have a way to re-compute the predictions from a certain point, It always does all the steps, so it's better to manage the dbs before running prokka for the first time. 

In a conda environment, `prokka` installs the dbs in `/path_to/miniconda3/envs/{env-name}/db`. You have to place the `hmpress` output files in  `/path_to/miniconda3/envs/{env-name}/db/hmm` , which should already have the `HAMAP` files included with `prokka`:

```sh
# check the output
$ prokka --listdb
[16:17:55] Looking for databases in: /data_1/jmaturana/miniconda3/envs/roary/db
[16:17:55] * Kingdoms: Archaea Bacteria Mitochondria Viruses
[16:17:55] * Genera: Enterococcus Escherichia Staphylococcus
[16:17:55] * HMMs: HAMAP pfam_N
[16:17:55] * CMs: Archaea Bacteria Viruses
```

**For the akkermansia dataset, prokka wasn't run with this extra db**

### 4. `hmm_mapper.py` from `eggnog-mapper`

The output files from `hmmpress` can be used with  `hmm_mapper.py`, which is included with `eggnog-mapper`.

```sh
hmm_mapper.py  -i $input  --cpu 8 --database $db /path/to/pfam_N.hmm -o $output --dbtype hmmdb 
```
pfam_N.hmm is the common preffix of the files created by `hmmpress`


### 5. Manually run `hmmscan/hmmsearch`

(todo)

```sh
$ hmmbuild Pfam_N.hmm Pfam-N
# idx name
 nseq alen mlen eff_nseq re/pos description
#---- -------------------- ----- ----- ----- -------- ------ -----------
...
11435 zinc_ribbon_5          264    86    47    64.88  1.173 zinc-ribbon domain
11436 zinc_ribbon_6           25    73    40     3.03  1.367 Zinc-ribbon
11437 zinc_ribbon_9         1028    94    61    49.78  0.916 zinc-ribbon
11438 zn-ribbon_14           189    60    30    78.79  1.795 Zinc-ribbon

# CPU time: 696.97u 3.58s 00:11:40.55 Elapsed: 00:05:33.47
```

From the Pfam blog:
> Pfam-N annotates 6.8 million protein regions into 11,438 Pfam families


So after download `Pfam-N.gz`, which is an alignment, `hmmbuild` has to be used with the uncompressed file. Then, a multi-fasta file can be used as target sequences, refered as sequence database:
```sh
$ hmmbuild pfam_N.hmm Pfam-N
# More cpus don't improve performance (hmmer4 comment in manual, i/o limited)
$ hmmsearch --domtblout hypo_akker_domtb.tsv --cpu 4 pfam_N.hmm ../hypothetical_proteins.fa 
```

But this requires more work to parse the result, check the length of the matches, see if multiple families match with a given single sequence, etc.