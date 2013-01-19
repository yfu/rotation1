#!/usr/bin/env perl

use strict;
use warnings;
use utf8;


# This script will try to figure out the go terms (or other annotation) that most frequently appear and I will use these go terms to plot the heatmap.
my %terms;                      # It will contain the terms (I will use go terms
                                # ) as the key and the times of appearance as
                                # the value.

sub by_value{
    $terms{$b} <=> $terms{$a};
}

my @files = glob "*.parsed.txt";
print "All the files I found: @files\n";
foreach ( @files ) {
    open FH, $_
        or die "I cannot open $_";
    print "$_ opened...\n";

    while ( <FH> ) {
       
        chomp;
        
        my @elements = split "\t";
        my $term = $elements[1];
        
        $terms{$term} += 1;
    }
}


my $counter = 0;

for ( sort by_value keys %terms ) {
    if ( /\AGO:/ ) {
        print "$_\t$terms{$_}\n";
        ++ $counter;
    }
    if ( $counter > 1000 ) {
        last;
    }
}
