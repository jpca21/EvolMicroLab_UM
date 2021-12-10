#! /usr/bin/env python

# Needs the Unix program `wc`. For Windows, see coretools. 

#Part of the standard library
from pathlib import Path
import subprocess as sp
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def raxml_part_to_nexus(in_file, out_file):
    in_file = Path(in_file)
    out_file = Path(out_file)
    #Simplest (and fast) way to get the number of lines of a file
    n_lines = int(sp.check_output(f'wc -l {in_file}', shell=True, 
                                  universal_newlines=True).split(' ')[0])
    if  out_file.exists():
        raise FileExistsError("Error: The nexus file already exists, this program is appending"
              " lines, so probably It's better to (re)move it first.")
    
    with open(in_file, 'r') as parth, open(out_file, 'a') as nexush:
        charpartition = []
        print('#nexus\nbegin sets;', file=nexush)
        for i, line in enumerate(parth):
            line_parts = line.strip().replace(',','').split(' ')
            print(f'    charset {line_parts[1]} = {line_parts[3]};', file=nexush)
            if i != n_lines - 1:
                charpartition.append(f'{line_parts[0]}:{line_parts[1]}, ')
            #The last line before writing the models ==> "charpartition mine ="
            else:
                charpartition.append(f'{line_parts[0]}:{line_parts[1]};')

    with open(out_file, 'a') as nexush:      
        models = "".join(charpartition)
        print(f'charpartition mine = {models}\nend;', file=nexush)
    
    return 0

def arg_parser(args):
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, 
                            description=('Receives as input the output from modeltest-ng,'
                                        ' which is a partition file compatible with'
                                        ' RaxML. Creates a nexus partition file, which is ' 
                                         ' compatible with IQ-Tree.')
                                         )
    parser.add_argument('in_file', help = "Name of the input partition file, coming from"
                        " modeltest-ng.")
    parser.add_argument('out_file', help = "Name of the output partition file,"
                        " " )

    args = parser.parse_args()
    
    return args

def main(args=None):
    args = arg_parser(args)
#     print(args)
    raxml_part_to_nexus(args.in_file, args.out_file)

if __name__ == "__main__":
    main()
