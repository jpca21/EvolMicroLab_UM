#! /usr/bin/env python


from pathlib import Path
from collections import defaultdict
import pickle
import re

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def arg_parser(args):
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, 
                            description='Parse the HHBlits (run against PDB) output files, and selects high'
                                         ' probability homologs structures. The threshold for selecting a'
                                         ' structure is based on the Probability column (check the hhsuite wiki.)'
                                         '  ')

    parser.add_argument('hhr_dir',
                        help = 'Input files. Directory where the output produced by HHBlits,'
                        ' .hhr files, are located.')
    parser.add_argument('out_dir',
                        help = 'Directory where the output pickle file, "high_prob.pkl", will be placed'
                        ' ')
    parser.add_argument('--prob_threshold', type=int, default=49, 
                        help = 'The threshold for selecting a pdb structure as a probable homolog.'
                        ' Value from the "Probability" column from hhblits')
    parser.add_argument('--glob', default='*.hhr', 
                        help = 'Glob used to get the input files in the hhr_dir, e.g. *pdb70.hhr. '
                        )
    args = parser.parse_args()
    
    return args

def parse_hhblits_table(file):
    
    with open(file, 'r') as fh:
        vals = []
        switch = False
        counter = 0
        for line in fh:
            if re.search(r'^\s+No Hit', line):
                switch = True
            elif switch:
#                 print(line)
                counter += 1
                vals.append(re.search(r'[0-9]\s+(\w+).+?\s+([0-9]+\.?[0-9]+)', line.strip()).groups())
#                 print(re.split('\s+', line))
            if counter == 3:
                break
    return vals


def select_pdbs(values, f, prob_tresh):
    '''
    values: A list of tuples coming from parse_hhblits_table()
    f: file to be parsed
    '''
    high_probs = defaultdict(list)
    for tup in values:
        prob = float(tup[1])
        pdb_id = tup[0].split('_')[0]
        print(f.stem, prob)
        if prob >= prob_tresh:
            print(pdb_id, prob)
            gene = '_'.join(f.stem.split('_')[:2])
            high_probs[gene].append((pdb_id, prob))
            break
    
    return high_probs

def main(args=None):
    args = arg_parser(args)
    prob = args.prob_threshold
    root = Path(args.hhr_dir)
    files = list(root.glob(args.glob))
    
    selected_high = []
    for f in files:
        values = parse_hhblits_table(f)
        high_probs = select_pdbs(values, f, prob)
        if high_probs:
            selected_high.append(high_probs)
        else:
            print(f'Gene {f.stem} does not have any high prob. structural homolog')

    out_dir = Path(args.out_dir)
    with open(out_dir.joinpath('high_prob.pkl'), 'wb') as fh:
        pickle.dump(selected_high, fh)

if __name__ == "__main__":
    main()
