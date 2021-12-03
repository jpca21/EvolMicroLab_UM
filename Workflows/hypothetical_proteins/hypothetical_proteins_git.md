```python
import pandas as pd
from pathlib import Path
from collections import defaultdict
import pickle
```

**For the original files, check the folder `/mnt/DATA/jmaturana/Hypothetical_proteins/`**:

- `akker_hypothetical.emapper.annotations` : `emapper` results using as input all the hypothetical proteins
- `akk_hypo_clu90-85.emapper.annotations` : `emapper` results using as input the cluster representatives from hypothetical proteins
- `akk_hypo_clu.tsv` : produced by `mmseqs createtsv`
-  `akk_hyp_clu90_85_rep.fasta` : produced by `mmseqs convert2fasta`


# Annotating genes

**Prokka** was used as the first software to predict and functionally annotate genes from the akkermansia dataset (201 genomes). Prokka predicted a total of **472481** proteins, of which  **263307 (55%) were annotated as *hypothetical protein***.  

Two sets of proteins were produced, depending on wether a protein is a *hypothetical protein* or not:


```python
faa_dir = Path("where/your/faas/are")
files = list(faa_dir.glob('*.faa'))
# Create an index with all the proteins sequences, needed to be built only once
faas_idx = SeqIO.index_db("akk_faas.idx", files, "fasta")
# How many genes in total?
len(faas_idx.values())
```




    472482




```python
## Create two sets of proteins. Each set has sequence records with all the info
#Generator
records = (faas_idx[name] for name in faas_idx)
rec_hypoth = []
rec_annot = []
for i, rec in enumerate(records):
    if ' '.join(rec.description.split(' ')[1:]) == 'hypothetical protein':
        rec_hypoth.append(rec)
    else:
        rec_annot.append(rec)

print(i, len(rec_hypoth), len(rec_annot))
```

    472481 263307 209175



```python
## Write the two sets of proteins into two multi-fasta files
with open('akk_hypothetical_proteins.fa', 'w') as fh:
    for seq in rec_hypoth:
        print(f'>{seq.description}\n{seq.seq}', file=fh)
with open('akk_annotated_proteins.fa', 'w') as fh:
    for seq in rec_annot:
        print(f'>{seq.description}\n{seq.seq}', file=fh)
```

**Eggnog-mapper**, `emapper.py`, was the second program used to functionally annotate these predicted proteins.

```sh
emapper.py --cpu 16 -i {1} --output {2} --output_dir $out_dir \
 -m diamond --sensmode very-sensitive --tax_scope 203494,74201,2 \
  --go_evidence all --target_orthologs all --dbmem --md5 --override
 ```
`--sensmode very-sensitive` was used to try to maximize the amount of annotated proteins.


**Eggnog-mapper** reports all the genes that have at least one type of annotation (any type). The more permissive annotation is usually/always Pfam (acts as a "lower barrier"). Given that the information of Pfam is too general to map directly to a specific function, many annotations aren't that useful without further investigation.



```python
def eggannot_to_df(annot_f):
    '''
    From the eggnog annotation file (`emapper.py`) to a dataframe
    (emapper v2.1.6)
    '''
    import pandas as pd
# ParserWarning: Falling back to the 'python' engine because the 'c' engine does 
# not support skipfooter; you can avoid this warning by specifying engine='python'.
    annot_df =  pd.read_csv(annot_f, sep='\t', skiprows=4, skipfooter=3,  na_values='-', engine='python')
    annot_df.rename({'#query':'query'}, axis=1, inplace=True)
    return annot_df
```


```python
root = Path("WD/for/this/project")
df = eggannot_to_df(root.joinpath("akker_hypothetical.emapper.annotations"))
df.info()
df.head(3)
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 180432 entries, 0 to 180431
    Data columns (total 22 columns):
     #   Column          Non-Null Count   Dtype  
    ---  ------          --------------   -----  
     0   query           180432 non-null  object 
     1   seed_ortholog   180432 non-null  object 
     2   evalue          180432 non-null  float64
     3   score           180432 non-null  float64
     4   eggNOG_OGs      180432 non-null  object 
     5   max_annot_lvl   180432 non-null  object 
     6   COG_category    150580 non-null  object 
     7   Description     150580 non-null  object 
     8   Preferred_name  18911 non-null   object 
     9   GOs             8197 non-null    object 
     10  EC              24362 non-null   object 
     11  KEGG_ko         62071 non-null   object 
     12  KEGG_Pathway    27155 non-null   object 
     13  KEGG_Module     16760 non-null   object 
     14  KEGG_Reaction   13423 non-null   object 
     15  KEGG_rclass     12658 non-null   object 
     16  BRITE           62071 non-null   object 
     17  KEGG_TC         14311 non-null   object 
     18  CAZy            6101 non-null    object 
     19  BiGG_Reaction   422 non-null     object 
     20  PFAMs           144009 non-null  object 
     21  md5             180432 non-null  object 
    dtypes: float64(2), object(20)
    memory usage: 30.3+ MB





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>query</th>
      <th>seed_ortholog</th>
      <th>evalue</th>
      <th>score</th>
      <th>eggNOG_OGs</th>
      <th>max_annot_lvl</th>
      <th>COG_category</th>
      <th>Description</th>
      <th>Preferred_name</th>
      <th>GOs</th>
      <th>EC</th>
      <th>KEGG_ko</th>
      <th>KEGG_Pathway</th>
      <th>KEGG_Module</th>
      <th>KEGG_Reaction</th>
      <th>KEGG_rclass</th>
      <th>BRITE</th>
      <th>KEGG_TC</th>
      <th>CAZy</th>
      <th>BiGG_Reaction</th>
      <th>PFAMs</th>
      <th>md5</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>IMCPJJDB_00001</td>
      <td>1396141.BATP01000047_gene3984</td>
      <td>2.270000e-04</td>
      <td>55.5</td>
      <td>COG3210@1|root,COG4625@1|root,COG3210@2|Bacteria,COG4625@2|Bacteria</td>
      <td>2|Bacteria</td>
      <td>T</td>
      <td>pathogenesis</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>PATR</td>
      <td>43a049a3d0554a052268595dace7e340</td>
    </tr>
    <tr>
      <th>1</th>
      <td>IMCPJJDB_00002</td>
      <td>349741.Amuc_0142</td>
      <td>4.470000e-52</td>
      <td>167.0</td>
      <td>COG3169@1|root,COG3169@2|Bacteria,46T5W@74201|Verrucomicrobia,2IUI9@203494|Verrucomicrobiae</td>
      <td>203494|Verrucomicrobiae</td>
      <td>S</td>
      <td>Putative member of DMT superfamily (DUF486)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko:K09922</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko00000</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>DMT_6</td>
      <td>2eb9da532c1846443a3d69d11296e378</td>
    </tr>
    <tr>
      <th>2</th>
      <td>IMCPJJDB_00003</td>
      <td>349741.Amuc_0473</td>
      <td>3.050000e-13</td>
      <td>77.0</td>
      <td>29SKQ@1|root,30DS1@2|Bacteria,46XQW@74201|Verrucomicrobia,2IWE1@203494|Verrucomicrobiae</td>
      <td>203494|Verrucomicrobiae</td>
      <td>S</td>
      <td>Aspartyl protease</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Asp_protease_2</td>
      <td>07e09a49b55be6707572e1ad485448d6</td>
    </tr>
  </tbody>
</table>
</div>



To get the annotations that are immediately useful, we select those which have being assigned a KEGG ortholog term, "KO":


```python
def get_not_nan(annot_file, col_names):
    '''
    For each column passed (list or tuple), obtain the "not_nan" values
    input: egnogg anotation file
    col_names example: [COG_category, KEGG_ko, PFAMs]
    '''
    
    df = eggannot_to_df(annot_file)
    for col in col_names:
        mask = df[col].notna()
        new_df = df[mask]
    return new_df
```


```python
new_df = get_not_nan(root.joinpath("akker_hypothetical.emapper.annotations"), ['KEGG_ko'])
print(new_df.shape)
new_df.head(3)
```

    (62071, 22)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>query</th>
      <th>seed_ortholog</th>
      <th>evalue</th>
      <th>score</th>
      <th>eggNOG_OGs</th>
      <th>max_annot_lvl</th>
      <th>COG_category</th>
      <th>Description</th>
      <th>Preferred_name</th>
      <th>GOs</th>
      <th>EC</th>
      <th>KEGG_ko</th>
      <th>KEGG_Pathway</th>
      <th>KEGG_Module</th>
      <th>KEGG_Reaction</th>
      <th>KEGG_rclass</th>
      <th>BRITE</th>
      <th>KEGG_TC</th>
      <th>CAZy</th>
      <th>BiGG_Reaction</th>
      <th>PFAMs</th>
      <th>md5</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>IMCPJJDB_00002</td>
      <td>349741.Amuc_0142</td>
      <td>4.470000e-52</td>
      <td>167.0</td>
      <td>COG3169@1|root,COG3169@2|Bacteria,46T5W@74201|Verrucomicrobia,2IUI9@203494|Verrucomicrobiae</td>
      <td>203494|Verrucomicrobiae</td>
      <td>S</td>
      <td>Putative member of DMT superfamily (DUF486)</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko:K09922</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko00000</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>DMT_6</td>
      <td>2eb9da532c1846443a3d69d11296e378</td>
    </tr>
    <tr>
      <th>3</th>
      <td>IMCPJJDB_00009</td>
      <td>349741.Amuc_0267</td>
      <td>1.310000e-42</td>
      <td>146.0</td>
      <td>COG1399@1|root,COG1399@2|Bacteria,46TBP@74201|Verrucomicrobia,2IURG@203494|Verrucomicrobiae</td>
      <td>203494|Verrucomicrobiae</td>
      <td>S</td>
      <td>Uncharacterized ACR, COG1399</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko:K07040</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko00000</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>DUF177</td>
      <td>3b4c8496b6004b1bef7395f4ea4447da</td>
    </tr>
    <tr>
      <th>9</th>
      <td>IMCPJJDB_00035</td>
      <td>1410613.JNKF01000012_gene1397</td>
      <td>4.310000e-75</td>
      <td>241.0</td>
      <td>COG1115@1|root,COG1115@2|Bacteria,4NDX7@976|Bacteroidetes,2FMFZ@200643|Bacteroidia</td>
      <td>2|Bacteria</td>
      <td>E</td>
      <td>amino acid carrier protein</td>
      <td>agcS</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko:K03310</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko00000</td>
      <td>2.A.25</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Na_Ala_symp</td>
      <td>76a490aebd66fcb337dcc3121576ff68</td>
    </tr>
  </tbody>
</table>
</div>



In this case, **62071** *hypothetical proteins* have been annotated with a proper function according to KEGG

### Clustering with `mmseqs`

As an alternative, this set of hypothetical proteins was clustered with `mmseqs` (see `clustering.sh`) and the representative sequences were passed to `emapper.py`.
The time of computation saved by using only the representative sequences isn't that relevant here, but for other software and/or for bigger datasets, this is recommended.

In this case, using a stringent clustering, `--cov-mode 0 -c 0.9 --min-seq-id 0.85`, **we obtained `29413` clusters (from more than 260 K sequences).**

#### Build a dictionary where keys are the representatives and the values are the members of each cluster 

This tsv comes from `mmseqs createtsv`, created by `clustering.sh`.


```python
clusters_map = hmmer_root.joinpath("akk_hypo_clu.tsv")
with open(clusters_map, 'r') as fh:
    lines = [l.strip() for l in fh.readlines()]

map_dic_hyp = defaultdict(list)
rep = None
for gene in lines:
    if gene.split('\t')[0] == rep:
        _ , member = gene.split('\t')
        map_dic_hyp[rep].append(member)
    else:
        rep, member = gene.split('\t')
        map_dic_hyp[rep].append(member)
len(map_dic_hyp.keys())
```




    29413



`akk_hyp_clu90_85_rep.fasta` are the representative sequences (`clustering.sh`)


```python
! egrep -c '>' $hmmer_root/akk_hyp_clu90_85_rep.fasta
```

    29413


### Read the `emapper.py` results

Here, we get **15K** results compared to the **180K** from using all the sequences. Later, this results will be propagated to all the member sequences (we are using the clusters' representatives)

**(`emapper.py` input was `akk_hyp_clu90_85_rep.fasta`)**


```python
df_hyp = eggannot_to_df(root.joinpath("akk_hypo_clu90-85.emapper.annotations"))
df_hyp.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 15573 entries, 0 to 15572
    Data columns (total 22 columns):
     #   Column          Non-Null Count  Dtype  
    ---  ------          --------------  -----  
     0   query           15573 non-null  object 
     1   seed_ortholog   15573 non-null  object 
     2   evalue          15573 non-null  float64
     3   score           15573 non-null  float64
     4   eggNOG_OGs      15573 non-null  object 
     5   max_annot_lvl   15573 non-null  object 
     6   COG_category    13199 non-null  object 
     7   Description     13199 non-null  object 
     8   Preferred_name  2270 non-null   object 
     9   GOs             1038 non-null   object 
     10  EC              2377 non-null   object 
     11  KEGG_ko         5529 non-null   object 
     12  KEGG_Pathway    2266 non-null   object 
     13  KEGG_Module     1293 non-null   object 
     14  KEGG_Reaction   1221 non-null   object 
     15  KEGG_rclass     1178 non-null   object 
     16  BRITE           5529 non-null   object 
     17  KEGG_TC         1139 non-null   object 
     18  CAZy            492 non-null    object 
     19  BiGG_Reaction   56 non-null     object 
     20  PFAMs           12776 non-null  object 
     21  md5             15573 non-null  object 
    dtypes: float64(2), object(20)
    memory usage: 2.6+ MB


### Propagate the annotations from the cluster representatives to the members' genes

We first select the genes which have a "KO" term assigned


```python
ko_annot_df = get_not_nan(root.joinpath("akk_hypo_clu90-85.emapper.annotations"), ['KEGG_ko'])
print(ko_annot_df.shape)
```

    (5529, 22)



```python
all_genes_anot = defaultdict()
for i, row in ko_annot_df.iterrows():
    for gene in map_dic_hyp[row['query']]:
        all_genes_anot[gene] = row['KEGG_ko']
len(all_genes_anot)
```




    62379




```python
# all_genes_anot['FNBKHHGP_00802']
all_genes_anot['GPIGBLJI_01391']
```




    'ko:K02913'



**We obtained a slightly higher number of genes annotated using the representative of each cluster, 62379, compared to the 62071 obtained when using the 260 K sequences.**
