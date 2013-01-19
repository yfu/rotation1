#! /usr/bin/python

# Created on 11/17/2012 by Yu Fu
# Run the get_peaks_range.py against all narrowPeak files

import os, glob
from subprocess import call

for file in glob.glob("*.narrowPeak"):
    call(['python', '../../bin/resize_bed.py', file, '250'])
    print "Finished processing %s"%file
