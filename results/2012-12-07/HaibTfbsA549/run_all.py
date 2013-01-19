#! /usr/bin/python

# Created on 11/17/2012 by Yu Fu
# Run the get_peaks_range.py against all narrowPeak files

import os, glob
from subprocess import call

for i in range(0, 75, 5):
    name = "hot" + str(i)
    filename = "hot" + str(i) + ".bed"
    command = ["peak2gene_output_gene_only.py", "-g", "../../../bin/peak2gene/hg19.refGene", "-n", name, "--op=all", "--symbol", "-d", "2000", "-t", filename]
    print command
    call(command)
    print "Finished processing %s"%file
