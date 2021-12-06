#! /usr/bin/env python


from pathlib import Path
from collections import defaultdict
import re

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def arg_parser(args):
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, 
                            description='Given the output from FastANI and two assemblies names,'
                                         ' returns the ANI between them.'
                                         )

    parser.add_argument('fastani_file',
                        help = 'FastANI output file (it should be a tsv file)'
                         ' ')
    parser.add_argument('assemblies', nargs=2,
                        help = 'Two assembly files, order does not matter. These should be the names present'
                         ' in the two first columns of the FastANI  table.')
    args = parser.parse_args()
    return args


def main(args=None):
    args = arg_parser(args)
    pat1, pat2 = [Path(pat).stem for pat in args.assemblies]
    print(f'Patterns used: {pat1} and {pat2}')
    switch = False
    with open(args.fastani_file, 'r') as fh:
        for i, line in enumerate(fh):
            if re.search(pat1, line) and re.search(pat2, line):
                print(line.split('\t')[2], f"at line {i + 1}")
                switch = True
        if not switch:
            print("The pair of assemblies isn't present in the FastANI table")


if __name__ == "__main__":
    main()