#! /usr/bin/env python

from collections import defaultdict
from os import sep
import pandas as pd
import pickle

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def arg_parser(args):
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, 
                            description='Takes the Annotation table from eggnog-mapper and creates a'
                                         ' table with counts for each COG category. This table can be easily plotted.'
                                         ' ')

    parser.add_argument('annotation_file', help = 'Annotation table from eggnog-mapper')
    parser.add_argument('output_file', help = 'Output file (TSV)')
    args = parser.parse_args()
    
    return args

cog_string = '''
INFORMATION STORAGE AND PROCESSING
[J] Translation, ribosomal structure and biogenesis
[A] RNA processing and modification
[K] Transcription
[L] Replication, recombination and repair
[B] Chromatin structure and dynamics

CELLULAR PROCESSES AND SIGNALING
[D] Cell cycle control, cell division, chromosome partitioning
[Y] Nuclear structure
[V] Defense mechanisms
[T] Signal transduction mechanisms
[M] Cell wall/membrane/envelope biogenesis
[N] Cell motility
[Z] Cytoskeleton
[W] Extracellular structures
[U] Intracellular trafficking, secretion, and vesicular transport
[O] Posttranslational modification, protein turnover, chaperones

METABOLISM
[C] Energy production and conversion
[G] Carbohydrate transport and metabolism
[E] Amino acid transport and metabolism
[F] Nucleotide transport and metabolism
[H] Coenzyme transport and metabolism
[I] Lipid transport and metabolism
[P] Inorganic ion transport and metabolism
[Q] Secondary metabolites biosynthesis, transport and catabolism

POORLY CHARACTERIZED
[R] General function prediction only
[S] Function unknown
'''

def eggannot_to_df(annot_f):
    '''
    From the eggnog annotation file (`emapper.py`) to a dataframe
    (emapper v2.1.6)
    '''

# ParserWarning: Falling back to the 'python' engine because the 'c' engine does 
# not support skipfooter; you can avoid this warning by specifying engine='python'.
    annot_df =  pd.read_csv(annot_f, sep='\t', skiprows=4, skipfooter=3,  na_values='-', engine='python')
    annot_df.rename({'#query':'query'}, axis=1, inplace=True)
    return annot_df

def multicat_to_single_counts(df):
    '''
    takes all the multi-category rows from the counts df and add them to their 
    respective single letter entries.
    '''
    
    split_counts = defaultdict(int)
    mc_df = df[df['COG_category'].str.len() > 1]
    
    for i, row in mc_df.iterrows():
        for cat in row['COG_category']:
            split_counts[cat] += row['counts']
    
    for k in split_counts.keys():
        df.loc[df['COG_category'] == k, 'counts'] += split_counts[k] 
    
    return df
    

def add_multcat_cog_to_one(df):
    '''
    Takes a df built by `eggannot_to_df` and creates a df with COG counts. Adds 
    the counts from entries that have assigned multiple COG categories to their 
    respective single letter categories. Renames not assigned entries,'-', to 'na'.
    Undercase letters are used because COG categories are uppercase
    '''
    cog_counts = df['COG_category'].value_counts().reset_index()
    cog_counts.rename({'index':'COG_category','COG_category':'counts'}, axis=1, inplace=True)
    
    # Add the counts from multicategories to single categories
    cog_counts = multicat_to_single_counts(cog_counts) #This is a dict
    
    #drop all the entries with multiple categories given those were already added
    cog_counts = cog_counts[cog_counts['COG_category'].str.len() == 1]
    cog_counts.reset_index(inplace=True, drop=True)
    
    #rename the not assigned entries, '-', to 'na'
    cog_counts.loc[cog_counts['COG_category'] == '-', 'COG_category'] = 'na'
    #order by counts
    cog_counts.sort_values(by='counts', ascending=False, inplace=True)
    return cog_counts

def cog_des_to_df(cog_string):
    
    '''
    Takes a string of COGs categories and their descriptions and returns a 
    DataFrame.
    '''
    
    cog_des = defaultdict()
    for line in cog_string.strip().split('\n'):
        if line.startswith('['):
            k = line.replace('[', '').replace(']', '').split(' ')[0]
            cog_des[k] = line.split(']')[1].strip()
                
    cog_des_df = pd.DataFrame.from_dict(cog_des, orient='index', columns=['COG description'])
    cog_des_df.loc['Na'] = 'Not assigned'
    
    return cog_des_df

def merg_des_counts(df):
    '''
    Merge descriptions with the counts df created by `multicat_to_single_counts()` 
    and concatenate (prefix) the COG descriptions with the single letter code to 
    make an "easier to understand" legend.
    Input: df by `eggannot_to_df()`
    Ouput: df ready to be plotted by seaborn/matplotlib
    '''
    
    cog_des_df = cog_des_to_df(cog_string)
    annot_agg_df = add_multcat_cog_to_one(df)
    annot_full_df = annot_agg_df.merge(cog_des_df, left_on='COG_category', right_index=True)
    annot_full_df['COG description'] = annot_full_df['COG_category'].str.cat(annot_full_df['COG description'], sep=' - ')
    total = annot_full_df['counts'].sum()
    annot_full_df['counts'] = (annot_full_df['counts'] / total) * 100
    annot_full_df.rename({'counts':'counts_%'},  axis=1, inplace=True)
    #here, change the 0 to another value if wanna drop a %
#     annot_full_df.drop(annot_full_df[annot_full_df['counts'] < 0].index, inplace=True)
#     annot_full_df['COG_category'] = annot_full_df['COG_category'].astype('category')
    annot_full_df.reset_index(drop=True, inplace=True)
    return annot_full_df

def main(args=None):
    args = arg_parser(args)
    anot_file = args.annotation_file
    output_file = args.output_file
    df = eggannot_to_df(anot_file)
    df_cogs = merg_des_counts(df)

    df_cogs.to_csv(output_file, index=False, sep='\t')

if __name__ == "__main__":
    main()
