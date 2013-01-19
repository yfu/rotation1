# #!/usr/bin/env perl
# use File::Basename;
use 5.012;

my $str = 'UwTfbsGm12865CtcfStdAlnRep0.narrowPeak';
$str = "SydhTfbsK562Corestsc30189IggrabAlnRep0.narrowPeak";
$str = "HaibTfbsHepg2Sp1Pcr1xAlnRep0.narrowPeak";
$str = "HaibTfbsEcc1Foxa1sc6553V0416102Dm002p1hAlnRep0.narrowPeak";


if( $str =~ m/\A([A-Z][a-z]+Tfbs[A-Z][a-z0-9]+[A-Z][a-z0-9]+)/) {

    print "Matched!\n";
    print "$1\n";
}
$_ = $str;

$_ =~ /GO/i;

