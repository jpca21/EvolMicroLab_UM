#! /usr/share/perl
use strict;
use Bio::LITE::Taxonomy;

### The following script is designed to improve the content of the `assembly_summary.txt`
### obtained from the NCBI Genome FTP repositories. This file contains enough information
### to obtain more taxonomic information, if we can use the `Bio::LITE::Taxonomy` module
### from Perl (https://metacpan.org/pod/Bio::LITE::Taxonomy)

### Optional: in some cases, this will be necessary.
### Use Lib to a specific address
use lib '/usr/local/share/perl/5.26.1';

### To execute this script, you will need a Database after install the module.
### Download it from here: ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdmp.zip
### (regular updates from this site are strongly recommended)
### Then, we will need to put the files in an specified directory
### (in this case, `/home/jpca/taxonomy/`)

my $taxDB = Bio::LITE::Taxonomy::NCBI->new (
                                            db=>"NCBI",
                                            names=> "/home/jpca/taxonomy/names.dmp",
                                            nodes=> "/home/jpca/taxonomy/nodes.dmp"
                                           );

### open the assembly_summary file, downloadable from NCBI Genomes FTP
### e.g., wget ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt

my $file = $ARGV[0] || "assembly_summary.txt";

### Opening the temporal file
open (A, $file) or die;
while (my $linea = <A>) {

  next if ($linea =~ /^#/);
  $linea =~ s/\n//;
  $linea =~ s/\r//;

  ### creating array from the line
  my @content = split ("\t", $linea);
  ### This column contains the tax_id
  my $taxid_d = $content[5];


  ### Defining taxonomic elements (`undef` if it is not defined)
  my $term_sking = $taxDB->get_term_at_level($taxid_d,"superkingdom") || "undef";
  my $term_phyl  = $taxDB->get_term_at_level($taxid_d,"phylum")  || "undef";
  my $term_class = $taxDB->get_term_at_level($taxid_d,"class")   || "undef";
  my $term_order = $taxDB->get_term_at_level($taxid_d,"order")   || "undef";
  my $term_fam   = $taxDB->get_term_at_level($taxid_d,"family")  || "undef";
  my $term_genus = $taxDB->get_term_at_level($taxid_d,"genus")   || "undef";
  my $term_sp    = $taxDB->get_term_at_level($taxid_d,"species") || "undef";

  ### Printing the line into the screen
  print "$linea\t$term_sking\t$term_phyl\t$term_class\t$term_order\t$term_fam\t$term_genus\t$term_sp\n";

}

close A;

### END.
exit;
