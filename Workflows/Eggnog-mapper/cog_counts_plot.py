#! /usr/bin/env python

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def arg_parser(args):
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, 
                            description='Takes the COG counts table from eggnog_to_cog_counts.py'
                                         ' and creates a bar plot.'
                                         ' ')

    parser.add_argument('cog_counts', help = 'Table with COG counts from eggnog_to_cog_counts.py')
    parser.add_argument('output_file', help = 'Output name. You must include the extension (.png or other)')
    args = parser.parse_args()
    
    return args

def plot_cog_cats(cog_counts, x='COG_category', y='counts_%', title= None, plot_name=None):
    
    '''
    Plots the cog_counts table. 
    Creates a vertical barplot for counts of COG categories. Colors are created by
    color paletes in seaborn
    Input: cog_counts table
    Output: Plot
    '''
    
    c_map = sns.color_palette('hls', 22, desat=0.9).as_hex()
    df = pd.read_csv(cog_counts, sep='\t')
    fig, ax = plt.subplots(figsize=(10,8))
    ax = sns.barplot(x = df[x],  y = df[y], hue = 'COG description',
                     data = df, palette=c_map,
                     ax=ax, dodge=False)
    plt.xlabel('COG categories', fontsize=18)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.ylabel('Counts %', fontsize=18)# fontname='source code Pro')
    plt.title(title, fontdict={'family':'Liberation Sans', 'size':20})

    # fontsize=14
    # legend works better with mono type because horizontal spacing is equal among lines
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1), 
               framealpha=0.8, prop={'family':'Source Code Pro', 'size':12})#, ncol=2)
    # # plt.ylabel(size=12)
    plt.xticks(rotation=60)
    ax.patch.set_facecolor('#ebebeb')
    fig.patch.set_facecolor('white')

    plt.tight_layout()

    return plt


def main(args=None):
    args = arg_parser(args)
    cog_counts = args.cog_counts
    output_file = args.output_file

    plt = plot_cog_cats(cog_counts)
    plt.savefig(args.output_file)

if __name__ == "__main__":
    main()
