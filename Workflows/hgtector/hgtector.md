# HGTector

This is valid for HGTector v2.0b2. Official repository here:

<https://github.com/qiyunlab/HGTector>

`hgtector` has 3 functions/sub-tools: `database`, `search` and  `analyze`,  which for a first run, should be used in that order.


## `database`

To build the database this instruction didn't work. It is in the official repository:

```
hgtector database --output <output_dir> --cats bacteria --sample 1 --rank species \
--reference --representative --compile diamond
```
`--sample 1` will sample one genome per species, by default is 0 so doesn't sample genomes.
`--rank` will set at which taxonomic rank the sampling will be performed, by default is `species`

I Tried other option too (nothing worked), useful ones are:
`--reference --representative` to add the reference and representative genomes, **after taxon sampling**. `--complete` it's also useful to download only complete genomes

The problem was that everytime, at a different point (different genome), the downloading process failed. I edited the source code of the program to obtain a table with the list of sampled genomes (line 518 in `database.py`):

```python
self.df.drop(columns=['al_seq', 'rc_seq'], inplace=True)
self.df.to_csv('table_path.csv', index=False)
```

See here for more details:

<https://github.com/qiyunlab/HGTector/issues/74>

(Months after I reported the error, the author responded, see the last post of the previous links**

You can download the genomes in the same folder the program uses by default,`download/faa/` and then you can run `database` again and the program will continue creating the needed files. It will check that all the genomes that were selected are in the expected folder so it won't download them again:


```terminal
hgtector database -o $db_dir --cats bacteria --sample 1 --rank species \
 --reference --representative
```

This will create the needed files for the compilation of the database, in this case the option `--compile` isn't used so you can compile the database in a separate step.
The last problema was the building the db took 149215692 KB of memory (149GB),so this must be ran in CONDOR. `analyze` and `search` require smaller amounts of memory so the should work in DARWIN. 

```terminal
echo $'accession\taccession.version\ttaxid' > prot.accession2taxid
zcat $taxon_map | awk -v OFS='\t' '{split($1, a, "."); print a[1], $1, $2}' >> prot.accession2taxid

diamond makedb --threads 24 --in $db_faa --taxonmap prot.accession2taxid.gz --taxonnodes taxdump/nodes.dmp --taxonnames taxdump/names.dmp --db diamond/db --log --verbose
```

This has to be run with `diamond 0.9.x` because the next step, `search`, will fail if `2.x` it's used. I used `0.9.36`.
The error has to do with the taxdump file created in the previous step, if one uses the taxdump downloaded from ncbi, `diamond 2.x` works with `analyze`. The NCBI's taxdump has all the species, so it about 7GB, while the one created by `database` should be less than 1GB. See here:

https://github.com/qiyunlab/HGTector/issues/76

## `search` 

Then, to search for proteins homologs of the input in the previoulsly created database:

```
parallel  -j3 "hgtector search -i {} -o search -m diamond -p 9 \
 --db $diamond_db -t $taxdump_dir" ::: $faas_dir/*_genomic.faa
```

With `gnu parallel` you can run one or multiple instances/jobs at a time, still it's convenient for parsing parameters
if you wanna run only one job at a time. The above instruction results in one command for each input file:

```
hgtector search -i genomes/GCF_900258535.1_PRJEB24722_genomic.faa -o search -m diamond -p 9  --db /data_1/jmaturana/hgtector_db/diamond/db.dmnd -t /data_1/jmaturana/hgtector_db/taxdump
```

## `analyze`

Then, you can `analyze` using as input the output of `search`

```terminal
taxdump_dir="/data_1/jmaturana/hgtector_db/taxdump"
search="/data_1/jmaturana/Blautia/hgtector/search0936"

## Each file will be proccessed with --bandwidth auto and grid
$ parallel --dry-run -j8 "hgtector analyze -i {1} -o analyze0936_self/{2}/{1/.} -t $taxdump_dir \
 --bandwidth {2} --self-tax 572511 --donor-name" ::: $search/*.tsv ::: auto grid
 ```

 Which results in:

```
$ hgtector analyze -i /data_1/jmaturana/Blautia/hgtector/search0936/GCF_900258535.1_PRJEB24722_genomic.tsv \
-o analyze0936_self/grid/GCF_900258535.1_PRJEB24722_genomic \
-t /data_1/jmaturana/hgtector_db/taxdump  --bandwidth grid --self-tax 572511 --donor-name
```
`analyze` is way faster than `search`.

- `auto` and `grid` gave similar results (but not equal)

- `--donor-name` writes taxa names instead of NCBI's taxa codes

