#! /usr/bin/env python


from pathlib import Path
from collections import defaultdict
import re, os
from ete3 import Tree
import pickle
import random
import string

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def arg_parser(args):
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, 
                            description='Takes the species tree from Orthofinder and converts its'
                                         ' leaves names to strings of 9 random characters. Writes this tree and'
                                         " a dictionary with the mappings in pickle format, so they can be used"
                                         " with 'ranger-dtl_pipeline.py'. It creates two Files:" 
                                         " 'species_tree_edited_rand_N0.nwk' and 'sname_to_rand.pkl'" 
                                         )

    parser.add_argument('species_tree', help = 'Species tree from Orthofinder.')
    parser.add_argument('out_dir', help = 'Output directory where the tree and dictionary will be placed.')
    args = parser.parse_args()
    
    return args

def get_random_string(length):
    # choose from any lowercase letters
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return(result_str)


def edit_specie_tree(tree_file):
    stree = Tree(tree_file, format= 1)
    #  dots have to be replaced by `_` to make it coincide with the gene trees' labels
    for node in stree.traverse():
        if node.is_leaf():
            node.name = re.sub(r'\.', '_', node.name)
    # Create the names to random str dictionary:
    n_leaves = len(stree.get_leaves())
    sname_to_rand = defaultdict()
    rand_strings = [get_random_string(9) for _ in range(n_leaves)]
    for l,rand in zip(stree.get_leaves(), rand_strings):
        sname_to_rand[l.name] = rand
    # convert the leaves' names using this dictionary
    for node in stree.traverse():
        if node.is_leaf():
            node.name = sname_to_rand[node.name]
    
    return (stree, sname_to_rand)

def main(args=None):
    args = arg_parser(args)
    stree, names_dict = edit_specie_tree(args.species_tree)
    stree_outf = 'species_tree_edited_rand.nwk'
    stree.write(format=1, outfile=stree_outf, dist_formatter='%f')
    stree_out2 = Path(args.out_dir).joinpath('species_tree_edited_rand_N0.nwk')
    # Add the N0 to the edited tree
    with open(stree_out2, 'w') as fh:
        print(Path(stree_outf).read_text().replace(';', 'N0;', 1), file=fh)
    os.remove(stree_outf)
    # Write the dictionary
    with open(Path(args.out_dir).joinpath('sname_to_rand.pkl'), 'wb') as fh:
        pickle.dump(names_dict, fh)

if __name__ == "__main__":
    main()
    