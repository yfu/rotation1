#!/usr/bin/env perl

use strict;
use warnings;

# This script will receive a parameter of the file name which contains GO terms
# as the first column.

# Given the times of appearance for each GO term, this script will go to each ".parsed.txt" file and find the p-values from binomial test and hypergeometric test.

# Then it will generate a table with the following format (please ignore the # symbol):

# TFname      binom-p hyper-p
# TF1   0.001 0.002
# TF2   0.003 0.004
# TF3   0.005 0.006

# This file can be fed into R and get the heatmap.
my $bh_flag=3;                # Change this to 3 if you want to use hyper
                                # p-value


my $limit = 100;                  # Limit the number of GO terms
my $counter = 0;                # For debugging, set it to a small value
                                # For real processing, set it to 100 or
                                # something like that.

my @files = glob "*.parsed.txt";
my @go_terms; # This array stores all the go terms that we are interested in
              # i.e. the "common" GO terms that appear significant in the output
              # of GREAT.
open GO_FH, shift @ARGV
    or die "Cannot open the given file!\n";

my $bh = shift @ARGV;

if ( $bh =~ /b|binom/i ) {
    $bh_flag = 2;               # Get binomial p-value
    # print 'binom';
} elsif ( $bh =~ /h|hyper/i ) {
    $bh_flag = 3;               # Get hypergeometric p-value
    # print 'hyper';
} else {
    die "Wrong option: you need to specify binom or hyper (b or h) as the option!\n";
}


while ( <GO_FH> ) {
    chomp;
    if ( /\A(GO:\d+)/ ) { # This is a GO term
        push @go_terms, $1;
        $counter ++ ;
    } else {
        next;                   # This is perhaps a comment line, ignore it.
    }
    if ( $counter >= $limit) {
        last;
    }
}


my $first_line = "\t" . (join "\t", @go_terms);
print $first_line; print "\n";
# print "@files";

# There are some annoying duplicate file names in which the only difference
# lies in the last few letters like:
#
# HaibTfbsA549GrPcr1xDex5nmAlnRep0.parsed
# HaibTfbsA549GrPcr1xDex50nmAlnRep0.parsed
#
# I decide to throw away those similar files and only keep the first one in
# alphabetical order
my @duplicates;


for my $f ( @files ) {
    open FH, $f;
    if ( $f =~ /BroadHistone/ ) {
        die "Wrong data! I cannot process this data. I can only process TF data!!\n";
    }
    my $this_tf_name = undef;
    if( $f =~ m/\A([A-Z][a-z]+Tfbs[A-Z][a-z0-9]+[A-Z][a-z0-9]+)/ ){
        if ( $1 ~~ @duplicates) {
            # print "Duplicates found: $1\n"; die "!!!!!";
            next;               # Ignore the annoying duplicates
        }
        
        $this_tf_name = $1;
        unshift @duplicates, $1;
    } else {
        print "$f is a strange file! I cannot sense if it contains TF data!\n"
    }
    # print "I am processing $this_tf_name...\n";

    # Create the hash and empty it. This hash stores GO terms as keys and p-
    # values (can be biono or hyper) as its values.
    my %hash;
    foreach ( keys %hash ) {
        delete $hash{$_};
    }
    # Build the hash using one of the "parse.txt" files.
    while ( <FH> ) {
        chomp;
        my @elements = split '\t';
        # print "$elements[1]";
        $hash{$elements[1]} = $elements[$bh_flag];
    }
    # Now search the hash for every GO term in go_terms array
    my $line = $this_tf_name . "\t";
    foreach ( @go_terms ) {
        if ( defined $hash{$_} ) {
            $line .= $hash{$_} . "\t";
        } else {
            $line .= 'NA' . "\t";
        }
    }
    print $line; print "\n";
    
}
