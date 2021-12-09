#! /usr/bin/env python


from pathlib import Path
from collections import defaultdict
import pickle
import re

import requests # used for getting data from a URL
from pprint import pprint # pretty print
from solrq import Q

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def arg_parser(args):
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, 
                            description='Takes as input the pickle file created by hhblits_select_pdbs.py'
                                         ' and creates a tsv table with columns gene, pdb and uniprot_id.'
                                         ' '
                                         )

    parser.add_argument('input_dir',
                        help = 'Directory where the pickle file created by hhblits_select_pdbs.py,'
                        ' high_prob.pkl, is located')
    parser.add_argument('out_table', default='*.hhr', 
                        help = 'output table name'
                        ' '
                        )
    args = parser.parse_args()
    
    return args

# the rest of the URL used for PDBe's search API.
search_url = "https://www.ebi.ac.uk/pdbe/search/pdb/select?"

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

def main(args=None):
    args = arg_parser(args)
    search_terms = Q(pdb_id="1bxw")


if __name__ == "__main__":
    main()