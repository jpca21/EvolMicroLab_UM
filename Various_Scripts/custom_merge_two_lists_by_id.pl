#!/usr/bin/perl
use strict;
use warnings;

##### ABOUT:
##### The following script was written to concatenate information from two
##### tab-separated tables containing information for a same identificator
##### (or, at least, one identificator in the first line with a shorter id
##### in the second one) 

my $file01 = $ARGV[0];
my $file02 = $ARGV[1];

### arrays to store files
my @file_A_content = ();
my @file_B_content = ();

### open and store first file
open (A, $file01) or die;
while (my $l1 = <A>) {
	$l1 =~ s/\n//g;
	$l1 =~ s/\r//g;
  next if ($l1 =~ /^#/);
  push @file_A_content, $l1;
}
close A;

### open and store second file
open (B, $file02) or die;
while (my $l1 = <B>) {
	$l1 =~ s/\n//g;
	$l1 =~ s/\r//g;
  next if ($l1 =~ /^#/);
  push @file_B_content, $l1;
}
close B;

### Observing and merging (the second file will
### be scanned according to each line from the first one)

LOOPA:
foreach my $la (@file_A_content) {
  my @ala = split ("\t", $la);
  my $idA = $ala[0];
  ### creating a new line, with all the info but without the ID
  shift(@ala);
  my $newA = join ("\t", @ala);

  LOOPB:
  foreach my $lb (@file_B_content) {
    my @alb = split ("\t", $lb);
    my $idB = $alb[0];
    ### creating a new line, with all the info but without the ID
    shift(@alb);
    my $newB = join ("\t", @alb);

    ### This match will consider that the ID from the second file
    ### is a substring from the ID in the first file
    if ($idA =~ /$idB/) {
      print "$idA\t$newA\t$newB\n";
      next LOOPA;
    } else {
      next LOOPB;
    }
  }
}


### END
exit;
