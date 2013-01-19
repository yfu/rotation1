#!/usr/bin/env perl

# This script will call great.pl to process each of the bed and narrowPeak file

use Cwd;

my $dir = shift @ARGV;          # Define the file path in url
opendir DH, cwd();
foreach ( readdir DH ) {
    chomp;
    print;
    
    next unless ( /(\.bed)|(\.narrowPeak)\Z/ );
    my $command = "great.pl http://zlab.bu.edu/$dir/$_";
    # print $command; print "\n";
    system $command;
    print "great.pl has finished its job now I will delete the tsv file.\n";

    my $current_file = $_;
    
    $current_file =~  s/\.bed\Z/.tsv/;
    print "I will delete $current_file\n";
    unlink $current_file; # Delete the current tsv file because it is too large
                          # sometimes
    
}
