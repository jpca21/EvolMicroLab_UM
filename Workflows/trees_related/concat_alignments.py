#! /usr/bin/env python

# This code takes as input a folder with alignments of the single copy orthogroups from
# orthofinder and concatenates them. It also creates a partition file for modeltest-ng,
# where each partition corresponds to a single orthogroup

# Requires biopython
try:
    from Bio.SeqIO.FastaIO import SimpleFastaParser
except ImportError:
    print("Biopython is required and it couldn't be imported")

#Part of the standard library
from pathlib import Path
from collections import defaultdict
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def arg_parser(args):
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter, 
                            description='Creates a concatenated alignment in fasta format'
                                         ' from a list of alignments in fasta format and'
                                         ' creates a partition file for it, where each'
                                         ' data block/partition corresponds to an individual'
                                         ' alignment.')

    parser.add_argument('genome_dir',
                        help = 'Directory containing all the genomes in fasta format.'
                        )
    parser.add_argument('aln_dir', 
                        help = 'Directory containing all the alignments in fasta format.')
    parser.add_argument('-ext', dest='ext', default='faa',
                        help = 'Extension of the fasta files inside genome_dir')
    parser.add_argument('-out_name', dest='out_name', default='concatenated',
                        help = "Prefix of the concatenated alignment and the partition file,"
                        " The suffixes 'fa' and '.part.txt' are added to the"   
                        " the alignment and the partition file respectively")
    args = parser.parse_args()
    
    return args

def concat_alignments(genome_dir, aln_dir, ext='faa', out_name='concatenated.fa'):
    
    genome_dir = Path(genome_dir)
    aln_dir = Path(aln_dir)
    uniq_id_fa = set()
    uniq_id_seq = []
    counter = 0
    out_name = Path(out_name)
    part_file = Path(f'{out_name}.part.txt')
    cat_file = Path(f'{out_name}.fa')
    if  cat_file.exists():
            raise FileExistsError("The concatenated alignment already exists, this program "
                "appends lines, so probably It's better to (re)move this file first."
                )
    if part_file.exists():
            raise FileExistsError("The partition file already exists, this program "
                    "is appending lines, so probably It's better to (re)move this file first."
                    )

    for aa in genome_dir.glob(f'*.{ext}'):
        counter += 1
        print(counter, aa.name)
        part_dic = defaultdict()
        uniq_id_seq = []
        uniq_id_fa = set()
        with aa.open('r') as aah:
            for faa_id, seq in SimpleFastaParser(aah):
                faa_uniq_id = faa_id.strip().split(' ')[0]
                uniq_id_fa.add(faa_uniq_id)
            for aln in aln_dir.glob('*.fa'):
                # read the alignment files while the genome is open
                with aln.open('r') as alnh:
                    for aln_id, seq in SimpleFastaParser(alnh):
                        aln_uniq_id = aln_id.strip()
                        if aln_uniq_id in uniq_id_fa:
                            uniq_id_seq.append(seq)
                            part_dic[aln_uniq_id] = len(seq)
                    # print(aln_id,len(seq))

        #Writes the sequences pertaining to a single genome, that's why is appended
            with open(cat_file, 'a') as cath:
                print(f'>{aa.stem}\n', f'{"".join(uniq_id_seq)}', 
                      sep='', file=cath)

    write_partition(part_dic, part_file)
        
    return 0


def write_partition(part_dic, part_file):
    start, end = (0,0)
    with open(part_file, 'a') as fh:
        item_ls = list(part_dic.items())
        for i, item  in enumerate(item_ls):
            if i == 0:
                start = 1
                end = item[1]
                part = f'PROT, {item[0]} = {start}-{end}'
                start = 0
                print(part, file=fh)
            else:
                start += item_ls[i-1][1]
                end = start + item[1]
                start_print = start + 1
                part = f'PROT, {item[0]} = {start_print}-{end}'
                print(part, file=fh)


def main(args=None):
    args = arg_parser(args)
#     print(args)
    concat_alignments(args.genome_dir, args.aln_dir, args.ext, args.out_name)

if __name__ == "__main__":
    main()