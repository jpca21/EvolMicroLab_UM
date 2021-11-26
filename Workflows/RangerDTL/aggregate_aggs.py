#! /usr/bin/env python


from pathlib import Path
from collections import defaultdict
import re, os
from ete3 import Tree
import pickle

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def arg_parser(args):
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, 
                            description='Takes the directory where the output from AggregateRanger is placed'
                                         " and creates a single summary table named 'nodes_events.tsv'."
                                         ' The table will be written into the parent folder of the aggregated files')

    parser.add_argument('aggregated_dir', help = 'Folder where all the aggregated files are located')
    parser.add_argument('snames_dict', help= 'Species names to random string dictionary (pickle).')
    parser.add_argument('n_seeds', type= int, help= 'Number of seeds used to run ranger-dtl')
    parser.add_argument('aggregate_bin', 
                                    help="Path to the AggregateRanger.linux file, which should be inside"
                                    " CorePrograms/ ")
    args = parser.parse_args()
    
    return args


### Translate back the aggregated files to the real species names and create a summary file,
### to encapsulate all the OGs/genes in a single file.
# 'stem_og' has the form: 'OG0000747_tree'

def main(args=None):
    args = arg_parser(args)
    agg_folder = Path(args.aggregated_dir)
    nodes_events = defaultdict(list)
    # Created the dictionary with all the relavant informtion from the agg files
    for agg_f in agg_folder.glob('agg_*tree.txt'):
        print(agg_f)
        og = agg_f.stem.split('_')[1]
        with open(agg_folder.parent.joinpath(f'new_{og}_tree.pkl'), 'rb') as ph:
            gname_dict = pickle.load(ph)
            trans = re.sub(r'(\w+)', lambda m: gname_dict.get(m.group(), m.group()), agg_f.read_text())
            # Translate the ids from the species trees
            with open(args.snames_dict, 'rb') as handle:
                names_dict = pickle.load(handle)
            inv_names = {v: k for k, v in names_dict.items()}
            trans = re.sub(r'(\w+)', lambda m: inv_names.get(m.group(), m.group()), trans)
            for a in re.finditer(r'\[(.+)\].+\[Speciations = ([0-9]+), Duplications = ([0-9]+), Transfers = ([0-9]+)\].+--> (.+), (\d+).+\]', trans):
                nodes_events[a.group(5)].append([a.group(1), a.group(2), a.group(3), a.group(4),a.group(6)])

    ###Writes the summary table ###
    n_seeds = args.n_seeds #number of seeds used with ranger-dtl
    total = n_seeds * 3 # 3 because that's the number of DTL combinations used with ranger-dtl
    out_f = Path('nodes_events.tsv')
    if out_f.exists():
        os.remove(out_f)
    with open(agg_folder.parent.joinpath('nodes_events.tsv'), 'a') as fh:
        print('node', 'genes', 'speciation_support', 'duplication__support', 'transfer_support', 'node_support', file=fh, sep='\t')
        for k,ls in nodes_events.items():
            for subls in ls:
                print(k, subls[0], int(subls[1])/total, int(subls[2])/total,
                        int(subls[3])/total, int(subls[4])/total, sep='\t', file=fh)

if __name__ == "__main__":
    main()
    