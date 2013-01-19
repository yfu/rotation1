#! /usr/bin/python
# This script is used to shrink the region of peaks simply because some peak 
# regions are too long to merge. Because if the original regions of peaks are 
# used, they can form a very long region when merged by mergeBed.
# The default length of the regions is 250 bp (i.e. +-125 bp up/downstream).
# The length is not a hard-coded parameter. You can define other length.


def shrink_peak_regions(filename, length):
    """This function will shrink the peak regions to length*2

filename is the input narrowPeak (bed) and length is the desired length of
the peak region
"""
    f = open(filename, 'r')
    for line in f.xreadlines():
        ele = line.split()
        start = int(ele[1])
        end = int(ele[2])
        length = end-start
        center = (start + end) / 2
        startn = center - length
        endn = center + length
        
