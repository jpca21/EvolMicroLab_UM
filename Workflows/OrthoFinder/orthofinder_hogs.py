#! /usr/bin/env python


from pathlib import Path
from collections import defaultdict
import pandas as pd
from ete3 import Tree
import shutil

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def arg_parser(args):
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, 
                            description='Selects and copies single-copy hierarchical orthogroups (HOGs),'
                                         ' present in all the genomes of a given node in the species tree'
                                         '  created by Orthofinder. Also, returns a list of HOGs present'
                                         ' in all the genomes but without taking into consideration'
                                         ' if they are single or multi-copy. (all_HOGs_present_in_all.list'
                                         ' inside the parent of out_dir)')

    parser.add_argument('nodes_dir',
                        help = 'Path to the directory containing all the Nx.tsv files,'
                        ' Phylogenetic_Hierarchical_Orthogroups.')
    parser.add_argument('node_to_use', 
                        help = 'Nx to be used, e.g: N50, N0, etc. (Upper or lower case allowed).'
                        ' To select this node, see the tree SpeciesTree_rooted_node_labels.txt'
                        ' inside `Species_Tree` directory')
    parser.add_argument('hogs_path', 
                        help = 'HOGs sequences path. This sequences should be created by'
                        ' the create_files_for_hogs.py included within the Orthofinder source code')
    parser.add_argument('tree_path', help = ' SpeciesTree_rooted_node_labels.txt path')
    parser.add_argument('-out_dir', default='Single_copy_HOGs',
                        help = 'Directory where the single-copy HOGs will be placed')
    args = parser.parse_args()
    
    return args


def selecting_ogs(nodes_dir, node_to_use, tree_path):
    '''
    Get all the OGs which are present in all the genomes belonging to a 
    specific node (node_to_use).

    nodes_dir: Path of the `Phylogenetic_Hierarchical_Orthogroups` directory.
    node_to_use: To select this node, see the tree in SpeciesTree_rooted_node_labels.txt 
    inside `Species_Tree` directory. It should be 'N50', 'N0', etc.
    tree_path: `SpeciesTree_rooted_node_labels.txt` path.
    '''
    nodes_dir = Path(nodes_dir)
    node_to_use = node_to_use.upper()
    node_to_use_file =  f'{node_to_use}.tsv'
    n_df = pd.read_csv(nodes_dir.joinpath(node_to_use_file), sep='\t', low_memory=False)
    global og_dict
    og_dict = defaultdict()
    
    # Build a dictionary where each key is an OG and each value is a dictionary
    # with genomes as keys and genes as values (a nested list of genes)
    for i, row in n_df.iterrows():
        genome_dict = defaultdict(list)
        # The genomes start in the column 4 (3:). Discard genomes
        # with no genes for a particular OG (NAs)
        for asm, gene in row[3:][row[3:].notna()].items():
            genome_dict[asm].append(gene.split(','))
        og_dict[row['OG']] = genome_dict
    
    print(f'Total number of OGs which are children of {node_to_use}: {len(og_dict.keys())}')
    tree = Tree(newick= tree_path, format=1)
    for node in tree.traverse():
        if node.name == node_to_use:
            n = node
    asms = n.get_leaf_names()
    number_asms = len(asms)
    print(f"The node {node_to_use} has {number_asms} genomes/leafs as children")
    
    # OGs present in all the genomes which belongs to this specific node 
    og_present_inall = []
    for og,v in og_dict.items():
        # the number of genomes (keys) has to be the same as the number of asms
        # keys can't be repetead, so this works
        if len(v.keys()) == number_asms:
            og_present_inall.append(og)

    return og_present_inall

def select_single_copy_hogs(og_present_inall):
#     i = 0 #for debugging
    hog_single_copy = []
    swt = False
    for og in og_present_inall:
        # if this loop get completed, the OG has only one 1 gene per genome
        for k,v in og_dict[og].items():
            # Flatten the nested list of genes
            genes = [gene for ls in v for gene in ls]
            if len(genes) == 1:
                swt = True
            # If a OG has more than one gene, start with the next OG
            if len(genes) > 1:
                swt = False
                break
        # The loop ended without break, so add the OG to the single copy OG list
        if swt:
#             i += 1
            hog_single_copy.append(og)
    
    return(hog_single_copy)

def copy_hogs(nodes_dir, hogs_path, node_to_use, tree_path, out_dir):
    '''
    Takes as input a list of hogs and copies them into out_dir.
    node_to_use: The N being used, without extension, e.g N50, N0, etc. (may be lower or upper case)
    out_dir: Destination directory.
    '''
    hogs_present_inall = selecting_ogs(nodes_dir, node_to_use, tree_path)
    hogs_single_copy = select_single_copy_hogs(hogs_present_inall)
    hogs_path = Path(hogs_path)
    node_to_use = node_to_use.upper()
    # Make the output dir if doesn't exist
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    for i,hog in enumerate(hogs_single_copy):
        hog_file = f'{node_to_use}.H{hog}.fa'
        hog_path = hogs_path.joinpath(hog_file)
        shutil.copy(hog_path, out_dir)
        
    assert (i + 1) == len(hogs_single_copy)
    print(f'Copied {len(hogs_single_copy)} HOGs to {out_dir}')
    return 0

def main(args=None):
    args = arg_parser(args)
#     print(args)
    copy_hogs(args.nodes_dir, args.hogs_path, args.node_to_use, args.tree_path, args.out_dir)
    hogs_present_inall = selecting_ogs(args.nodes_dir, args.node_to_use, args.tree_path)
    with open(f'{Path(args.out_dir).parent.joinpath("all_HOGs_present_in_all.list")}', 'w') as fh:
        for hog in hogs_present_inall:
            print(hog, file=fh)

if __name__ == "__main__":
    main()