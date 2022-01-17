#!/usr/bin/perl
use strict;
use warnings;

#### This script can be used to download GBFF.GZ files from the directories indicated in the genome list from
#### `assembly_summary.txt` files; for example, if you download the archaeal summary file executing:
#### `wget https://ftp.ncbi.nlm.nih.gov/genomes/refseq/archaea/assembly_summary.txt`
#### you can use this script to download all files, or making a previous filter, for example:
#### `cat assembly_summary.txt | grep "Ferroplasma" > list`
#### `perl downloader_from_assembly_summary.pl list`

#### This script uses `wget`

my $file01 = $ARGV[0] || "assembly_summary.txt";

open (B, $file01) or die;

DATA_LOOP:
while (my $l1 = <B>) {
	$l1 =~ s/\n//g;
	$l1 =~ s/\r//g;
	(next DATA_LOOP) if ($l1 =~ /^#/); ### omit first line

	##### Parsed tabulated file and reconstructing filename 
	my @matrix_1 = split ("\t", $l1);
	my $A = $matrix_1[0];
	my $B = $matrix_1[15];
	$B =~ s/ /_/g;
	my $url = $matrix_1[19];
	my $neoUrl = "$url/$A\_$B\_genomic.gbff.gz";
	print "$neoUrl\n";

	#### DOWNLOADING
	system ("wget -q -nc -t 10 --wait=10 --limit-rate=1024K $neoUrl");
}

close B;

exit;
