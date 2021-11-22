#! /usr/bin/env python

from pathlib import Path
from collections import defaultdict
from ete3 import Tree
from collections import defaultdict

from argparse import ArgumentParser
from argparse import  ArgumentDefaultsHelpFormatter

def arg_parser(args):
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, 
                            description="Creates a list of assemblies' names from a list of node(s)."
                                         ' These nodes are from the species tree created by OrthoFinder'
                                         ' and for each node, a list of all children leaves of the particular node '
                                         ' will be created. Each output file is named {node}_genome.list'
                                         )

    parser.add_argument('species_tree',
                        help = 'Path to the species tree created by OrthoFinder')
    parser.add_argument('nodes', nargs="*", type=str,
                            help = 'List of target nodes.  To select these nodes, see the'
                        ' SpeciesTree_rooted_node_labels inside Species_Tree/ directory'
                        ' E.G.: N33 N22 N12')
    parser.add_argument('-out_dir', default='.',
                        help = 'Directory where the single-copy HOGs list will be written')
    args = parser.parse_args()
    
    return args

def get_genomes_from_node(node_list, tree_file):
    '''
    node_list: List or tuple with the node names. e.g. [N8, N33]
    '''
    tree = Tree(tree_file, format=1)
    node_asms = defaultdict()
    for n in node_list:
        for node in tree.traverse():
            if node.name == n:
                print(f'number of genomes for node {n}: {len(node.get_leaf_names())}\n')
                node_asms[n] = node.get_leaf_names()
    return node_asms


def main(args=None):
    args = arg_parser(args)
    node_list = args.nodes
    node_asms = get_genomes_from_node(node_list, args.species_tree)
    out_dir = Path(args.out_dir)
    for node,asms in node_asms.items():
        out_f = f'{node}_genome.list'
        if Path(out_f).exists():
            raise FileExistsError(f"The file {out_f} already exists, this program is "
                                          "appending lines, so you have to (re)move it first."
                                         ) 
        with open(out_dir.joinpath(out_f), 'a') as fh:
            for asm in asms:
                print(asm, file=fh)

if __name__ == "__main__":
    main()