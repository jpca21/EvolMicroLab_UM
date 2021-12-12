#! /usr/bin/env python

from collections import defaultdict
import pickle
import re
import Bio.KEGG.REST as kgrest
from bioservices import UniProt
## PDBe
import requests # used for getting data from a URL
from solrq import Q # used to turn kresult queries into the right format

# The code to use the PDBe API comes from https://github.com/PDBeurope/pdbe-api-training 
# notebook 6_PDB_search.ipynb

# The URL used for PDBe's search API.
search_url = "https://www.ebi.ac.uk/pdbe/search/pdb/select?"



from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def arg_parser(args):
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, 
                            description='Maps PDB Ids from hhblits to Uniprot, KEEG genes and'
                                         ' orthologs (KOs). '
                                         '  49'
                                         ' ')

    parser.add_argument('pickle_file',
                        help = 'Pickle file, "high_prob.pkl", created by hhblits_select_pdbs.py')
    parser.add_argument('out_table', 
                        help = "Output tsv table")
    args = parser.parse_args()
    return args


def make_request(search_dict, number_of_rows=10):
    """
    makes a get request to the PDBe API
    :param dict search_dict: the terms used to search
    :param number_of_rows: number or rows to return - limited to 10
    :return dict: response JSON
    """
    if 'rows' not in search_dict:
        search_dict['rows'] = number_of_rows
    search_dict['wt'] = 'json'
    # pprint(search_dict)
    response = requests.post(search_url, data=search_dict)

    if response.status_code == 200:
        return response.json()
    else:
        print("[No data retrieved - %s] %s" % (response.status_code, response.text))

    return {}


def format_search_terms(search_terms, filter_terms=None):
    ret = {'q': str(search_terms)}
    if filter_terms:
        fl = '{}'.format(','.join(filter_terms))
        ret['fl'] = fl
    return ret


def run_search(search_terms, filter_terms=None, number_of_rows=100):
    search_term = format_search_terms(search_terms, filter_terms)

    response = make_request(search_term, number_of_rows)
    results = response.get('response', {}).get('docs', [])
    print('Number of results: {}'.format(len(results)))
    if not len(results): # Added
        pdb_no_result = search_terms.query.raw
        print('search term with no result:', pdb_no_result)
    return results


def build_table(pickle_file, out_table):
    '''
    pickle_file: Pickle file, list of dicts from select_pdbs(), created by hhblits_select_pdbs.py
    '''
    
    with open(pickle_file, 'rb') as fh:
        selected_pdbs = pickle.load(fh)

    with open(out_table, 'w') as fh:
        print('gene\tpdb_id\tuniprot_acc\tuniprot_id\tkegg_gene\tKO', file=fh)

    for d in selected_pdbs:
        uacc = ''
        uid = ''
        kegg_gene = ''
        ko = ''
        for gene, vals in d.items():
            pdb_id = vals[0][0].lower()
            search_terms = Q(pdb_id=pdb_id)
            filter_terms = ['entry_uniprot_accession', 'entry_uniprot_id']
            results = run_search(search_terms,filter_terms=filter_terms)
#             results may be [{}]
            if results[0]:
                uacc = results[0]['entry_uniprot_accession'][0]
                uid = results[0]['entry_uniprot_id'][0]
                u = UniProt()
                d = u.mapping(fr='ID', to='KEGG_ID', query=uacc)
                if d:
                    kegg_gene = d[uacc][0] #1st element of the values
                    kresult = kgrest.kegg_link("ko", kegg_gene).read().strip()
                    if kresult:
                        ko = kresult.strip().split('\t')[1]
                    else:
                        print(f"the KEGG gene {kegg_gene} didn't return a valid result")
                        ko = ''
            # Write empty strings when there isn't a valid result
            else:
                print(f"Results is empty: {results}")
            with open(out_table, 'a') as fh:
                print(gene, pdb_id, uacc, uid, kegg_gene, ko,
                      file=fh, sep='\t')


def main(args=None):
    args = arg_parser(args)
    pickle_file = args.pickle_file
    out_table = args.out_table

    build_table(pickle_file, out_table)


if __name__ == "__main__":
    main()
