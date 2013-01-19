#! /usr/bin/python
# Calculate the distributution of length of peaks, given a narrowPeak (bed) file

import os, sys

def get_peak_range(src, dest):
    # Read in a file named "filename.sfx" and output it to a file named "filename_peak_range.txt"
    f = open(src, 'r')
    direAndFilename, suffix = os.path.splitext(src)
    _, filename = os.path.split(direAndFilename) # Only the filename
    output_fn = os.path.join(dest, filename) + "_peak_range.txt" # where to output the result
    print ""
    print "I will save the result here:", output_fn
    f_out_1 = open(output_fn, 'w')
    num_features = 0
    for line in f.xreadlines():
        num_features += 1
        ele = line.split()
        start = int(ele[1])
        end = int(ele[2])
        length = end - start
        print >> f_out_1, length
    print "The number of features in %s is %d."%(filename, num_features)
    f.close()
    f_out_1.close()
    
    print "Done! Please check %s in your directory!"%output_fn
    print ""
    
    return output_fn

    
def main():
    if len(sys.argv)!=3:
        print "Usage: python %s input_bed_file output_result"
        exit(-1)
    fn = get_peak_range(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()