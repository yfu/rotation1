#!/usr/bin/env perl
# When running this script, you need to switch to the directory that containts
# the bed files. This script will automatically generate bed files of different
# hotnesses and call GREAT by its API. Also, you need to make sure that
# this folder is accessible (i.e. it is from on a server) for GREAT so that GREAT can obtain the bed files
# it need.

use strict;
use warnings;
use 5.012;
use URI::Split qw(uri_split uri_join);
use URI::Escape;
use File::Basename;
use File::Spec;
use Cwd;


my %features;

sub gen_hot_bed {
    # This function will get the bed filename (the 1st param) and a list of
    # hotness (the 2nd param) e.g. qw/10 20 30 40 50/ and 10 means 10% of the
    # original peaks while 95 means 95% of the original peaks
    print '-' x 80; print "\n";
    print "I am generating bed files with different hotnesses and save name to the current directory"; print "\n";
    my $filename = shift @_;
    my @hotnesses = @_;
    print "You select HOTness:@hotnesses\n";

    delete @features{ keys %features };
    open FH, '<', $filename;
    # This hash saves the line as the key and hotness as the value
    
    while ( <FH> ) {
        chomp;
        # print;                  # For debugging purpose
        my @elements = split;
        my $chrom = $elements[0];
        my $start = $elements[1];
        my $end = $elements[2];
        if ( scalar @elements == 3) {
            $features{"$chrom\t$start\t$end\n"} = undef;
        } else {
            my $hotness = $elements[3];
            $features{"$chrom\t$start\t$end\t$hotness\n"} = $hotness;
        }
    }
    foreach my $h ( @hotnesses ) {
        my @sorted = sort by_signal keys %features;
        open W, '>', "hot${h}.bed";
        for ( @sorted) {
            if ( $features{$_} >= $h ) {
                print W;                
            }

        }
        close W;
    }
    print '-' x 80; print "\n";
}


sub by_signal{
    $features{$a} <=> $features{$b};
}

sub call_great {
    # specify the url for bed files and the
    my $result_file = 
    my $great_url = "http://bejerano.stanford.edu/great/public/cgi-bin/greatStart.php";
    my $great_params = "outputType=batch&requestSpecies=hg19&requestName=Yu&requestSender=myClient&";
    
    my $bed_url = shift @_;
    
    my ($schema, $auth, $path) = uri_split($bed_url);
    $result_file = basename $path, qw(.bed .narrowPeak);
    $result_file .= '.tsv';
    print "Result for the original bed file will be saved in this file: $result_file\n";
    $bed_url = uri_escape $bed_url;
    my @hotnesses = @_;
    my $command = "wget -O $result_file \"$great_url?${great_params}requestURL=$bed_url\"";
    print "I will call great using this command: \n$command"; print "\n";
    system $command;
    
    for ( @hotnesses ) {
        # I decide that the function should be able to handle the splitting
        # and joining so that this function itself will be more robust.
        my $dirname = dirname $path;
        my $filename = 'hot' . $_ . '.bed';
        my $result_file = 'hot' . $_ . '.tsv';
        my $bed_url = File::Spec->catfile($dirname, $filename);
        $bed_url = uri_join($schema, $auth, $bed_url);
        print "Result for bed$_.hot will be saved in this file: $result_file\n" ;
        $bed_url = uri_escape $bed_url;
        my $command = "wget -O $result_file \"$great_url?${great_params}requestURL=$bed_url\"";
        print "I will call GREAT using this command: \n$command\n";
        system $command;       
    }
}

sub parse {
    # This function does not need any parameters. It will parse all the tsv files in current directory. This function has hardcoded values: it will extract
    # p-values of hyper and bionom only. And these two values are from
    # column .
    my %col = ( "Ontology" => 0,
                "ID" => 1,
                "BinomBonfP" => 5,
                "HyperBonfP" => 14);
    opendir DH, getcwd();
    foreach ( readdir DH ) {
        chomp;
        next unless ( /\.tsv\Z/ ); # If this is not a tsv file, just skip it
        my $current_tsv = $_;       # I save it here because I would like to
                                # use it in the following loop, in which
                                # the $_ is overridden by the current line
        open FH, $current_tsv; # filehandle for the current tsv file
        my $new_filename = s/\.tsv\Z/.parsed.txt/r; # Generate the filenae
                                # for the parsed results.
        open PARSED, '>', $new_filename;
        print PARSED "Ontology\tID\tBinomBonfP\tHyperBonfP\n";
        while ( <FH> ) {
            next if ( /\A(#|\s+)/ );  # If this line starts with a '#',
                                # ignore it.
            chomp;
            # print "!!!$_";
            
            # split the current string, get a splice, then join the
            # strings ussing join and print to the filehandle
            my @columns = split "\t", $_;
            # print $columns[1];
            @columns = @columns[0, 1, 5, 14];
            # print "@columns";
            
            my $newline = join "\t", @columns;
            $newline .= "\n";
            print PARSED $newline;
            # print PARSED (join "\t", @columns);
        }
    }
}

# Call the script like this:
# perl great.pl -p "http://www.example.com/Broad/test.bed" 10 20 30
# option 'p' means parsing (processing) the tsv files directly without
# calling GREAT. If there is an option 'p', then the program will NOT
# call GREAT and parse only. When using option 'p', you do not need to
# specify the HOTnesses.

# If the current directory already contains tsv files, this script will
# simply try parse them without calling GREAT.
# If no tsv file(s) exists, this script will call great and then parse
# the files.

print '-' x 80; print "\n";
if ( $ARGV[0] eq '-p') {
    print "So you want to parse tsv files only!\n";
    print "I will process them directly without calling GREAT!\n";
    print "If you want to call GREAT to process the file, \n";
    print "please do not use option '-p'.\n";
    print "Begin parsing...\n";
    print '-' x 80; print "\n";
    &parse;                     # Will parse all tsv files in current dir
    exit 0;
}


my $url = shift @ARGV;
my ($schema, $auth, $path) = uri_split($url); #extract the domain, path and file
my $filename = basename($path);
print "The domain name is $auth\n";
print "The path is $path\n";

print "The bed filename is $filename"; print "\n";
my @hotnesses = @ARGV;          # The parameters left are all hotnesses like
                                # 10 20 30
gen_hot_bed $filename, @hotnesses;
&call_great( $url, @hotnesses );
parse $filename;


say '-' x 80;
