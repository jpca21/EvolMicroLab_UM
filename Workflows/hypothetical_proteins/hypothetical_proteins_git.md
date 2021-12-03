```python
import pandas as pd
from pathlib import Path
from collections import defaultdict
import pickle
```

**For the original files, check the folder `/mnt/DATA/jmaturana/Hypothetical_proteins/` @coyhaique**:

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
ko_annot_all_df = get_not_nan(root.joinpath("akker_hypothetical.emapper.annotations"), ['KEGG_ko'])
print(ko_annot_all_df.shape)
ko_annot_all_df.head(3)
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

### Are there representative genes that were annotated with "KO" terms, but they weren't when all the sequences were used?


```python
ko_annot_all_df.shape
```




    (62071, 22)




```python
ko_annot_df.shape
```




    (5529, 22)




```python
print(ko_annot_df[(ko_annot_df['query'].isin(ko_annot_all_df['query'] ))].shape)
ko_annot_df[~(ko_annot_df['query'].isin(ko_annot_all_df['query'] ))]
```

    (5521, 22)





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
      <th>1044</th>
      <td>KBNPILAJ_01176</td>
      <td>349741.Amuc_1548</td>
      <td>1.580000e-07</td>
      <td>62.0</td>
      <td>COG0666@1|root,COG0666@2|Bacteria</td>
      <td>2|Bacteria</td>
      <td>G</td>
      <td>response to abiotic stimulus</td>
      <td>legA</td>
      <td>NaN</td>
      <td>3.5.1.2</td>
      <td>ko:K01425</td>
      <td>ko00220,ko00250,ko00471,ko01100,ko04724,ko04727,ko04964,ko05206,ko05230,map00220,map00250,map00471,map01100,map04724,map04727,map04964,map05206,map05230</td>
      <td>NaN</td>
      <td>R00256,R01579</td>
      <td>RC00010,RC02798</td>
      <td>ko00000,ko00001,ko01000</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Ank_2,Ank_4,Peptidase_M48</td>
      <td>643ca514eeb0dd574553b86055a60711</td>
    </tr>
    <tr>
      <th>3294</th>
      <td>LIHBKOGP_02244</td>
      <td>349741.Amuc_0428</td>
      <td>2.530000e-04</td>
      <td>50.1</td>
      <td>COG3210@1|root,COG3210@2|Bacteria</td>
      <td>2|Bacteria</td>
      <td>U</td>
      <td>domain, Protein</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko:K20276</td>
      <td>ko02024,map02024</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko00000,ko00001</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>DUF4347,Haemagg_act,PATR</td>
      <td>9a08ca78d4e94862f437252bede9537a</td>
    </tr>
    <tr>
      <th>5725</th>
      <td>IMCPJJDB_00386</td>
      <td>349741.Amuc_0088</td>
      <td>1.710000e-32</td>
      <td>142.0</td>
      <td>COG3307@1|root,COG3307@2|Bacteria</td>
      <td>2|Bacteria</td>
      <td>M</td>
      <td>-O-antigen</td>
      <td>NaN</td>
      <td>GO:0003674,GO:0003824,GO:0005575,GO:0005623,GO:0005886,GO:0006464,GO:0006486,GO:0006807,GO:0008150,GO:0008152,GO:0009058,GO:0009059,GO:0009100,GO:0009101,GO:0009987,GO:0016020,GO:0016021,GO:0016740,GO:0016757,GO:0019538,GO:0031224,GO:0034645,GO:0036211,GO:0043170,GO:0043412,GO:0043413,GO:0044237...</td>
      <td>NaN</td>
      <td>ko:K02847,ko:K13009,ko:K16705</td>
      <td>ko00540,ko01100,map00540,map01100</td>
      <td>M00080</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko00000,ko00001,ko00002,ko01000,ko01005,ko02000</td>
      <td>9.B.67.4,9.B.67.5</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>PglL_A,Wzy_C,Wzy_C_2</td>
      <td>a736117b86caa539879ac58c1ad3aa5a</td>
    </tr>
    <tr>
      <th>9992</th>
      <td>IGCHHHLL_00202</td>
      <td>349741.Amuc_2163</td>
      <td>1.880000e-08</td>
      <td>63.9</td>
      <td>COG0790@1|root,COG0790@2|Bacteria</td>
      <td>2|Bacteria</td>
      <td>S</td>
      <td>beta-lactamase activity</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko:K07126,ko:K13582</td>
      <td>ko04112,map04112</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko00000,ko00001</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>MORN_2,Peptidase_C14,Pkinase,Sel1</td>
      <td>557fd7683bea95d5d38f1f58366cd0ea</td>
    </tr>
    <tr>
      <th>10036</th>
      <td>GFNMCGMP_01192</td>
      <td>661367.LLO_2649</td>
      <td>7.920000e-11</td>
      <td>69.7</td>
      <td>COG0790@1|root,COG0790@2|Bacteria,1MWPA@1224|Proteobacteria,1RPI3@1236|Gammaproteobacteria,1JCSU@118969|Legionellales</td>
      <td>2|Bacteria</td>
      <td>S</td>
      <td>Sel1-like repeats.</td>
      <td>enhC</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko:K07126,ko:K15474</td>
      <td>ko05134,map05134</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko00000,ko00001</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Sel1</td>
      <td>c8f64d62d86d067d4c21f56da316fba7</td>
    </tr>
    <tr>
      <th>11765</th>
      <td>PMKGNBDP_01896</td>
      <td>349741.Amuc_1063</td>
      <td>3.230000e-15</td>
      <td>85.9</td>
      <td>COG0666@1|root,COG0666@2|Bacteria</td>
      <td>2|Bacteria</td>
      <td>G</td>
      <td>response to abiotic stimulus</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko:K06867,ko:K07001</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko00000</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Ank,Ank_2,Ank_4,Ank_5,Fic,Sel1</td>
      <td>5e17ef8d1da7f59869599c284999efd3</td>
    </tr>
    <tr>
      <th>13506</th>
      <td>PGIFDEOE_01613</td>
      <td>1123054.KB907707_gene2166</td>
      <td>5.270000e-05</td>
      <td>53.5</td>
      <td>COG4591@1|root,COG4591@2|Bacteria,1MVV7@1224|Proteobacteria,1RMP9@1236|Gammaproteobacteria,1WW0V@135613|Chromatiales</td>
      <td>2|Bacteria</td>
      <td>M</td>
      <td>lipoprotein releasing system, transmembrane protein, LolC E family</td>
      <td>lolC</td>
      <td>GO:0003674,GO:0005215,GO:0005575,GO:0005623,GO:0005886,GO:0006810,GO:0008104,GO:0008150,GO:0008565,GO:0015031,GO:0015833,GO:0016020,GO:0016021,GO:0031224,GO:0032991,GO:0033036,GO:0034613,GO:0042886,GO:0042953,GO:0042954,GO:0044425,GO:0044459,GO:0044464,GO:0044872,GO:0044873,GO:0044874,GO:0045184...</td>
      <td>NaN</td>
      <td>ko:K02004,ko:K09808</td>
      <td>ko02010,map02010</td>
      <td>M00255,M00258</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko00000,ko00001,ko00002,ko02000</td>
      <td>3.A.1,3.A.1.125</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>FtsX,MacB_PCD</td>
      <td>f55bc46bd0cc7e8ec1d973e3d097b6dc</td>
    </tr>
    <tr>
      <th>15409</th>
      <td>GFNMCGMP_00211</td>
      <td>471857.Svir_21100</td>
      <td>9.410000e-04</td>
      <td>48.5</td>
      <td>COG0666@1|root,COG0666@2|Bacteria,2IIAC@201174|Actinobacteria,4E4DI@85010|Pseudonocardiales</td>
      <td>2|Bacteria</td>
      <td>S</td>
      <td>Ankyrin repeat-containing protein</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko:K06867</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>ko00000</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Ank,Ank_2,Ank_4,Ank_5</td>
      <td>f4f390b6597f6d3de269e4d1825adf50</td>
    </tr>
  </tbody>
</table>
</div>



**There are 8 cluster representative's sequences that weren't annotated when using all the sequences**


```python

```
