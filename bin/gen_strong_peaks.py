#! /usr/bin/python

import sys
import os
def return_strong_peaks(file, perc):
    dic = {} # line as the key, strength as the value
    for line in file.xreadlines():
        elements = line.split()
        strength = float(elements[6])
        # print strength
        dic[line] = strength
    
    sorted_lines = sorted(dic.keys(), key=lambda x: -dic[x])
    length = len(sorted_lines)
    return sorted_lines[:int(length*perc)]

def gen_strong_peaks(filename, cutoffs):
    
    survival_david = {}
    
    for cutoff in cutoffs:
        # Generate a sequence of 0.05, 0.1, 0.15, 0.2, 0.25
        # You can change the step to generate different gredients.
        print "Use the strongest %f%% peaks" % (cutoff*100)
        file = open(sys.argv[1], 'rU')
        strong_lines = return_strong_peaks(file, cutoff)
        # print strong_lines
        base, _ = os.path.splitext(sys.argv[1])
        f_o = open(str(cutoff)+".txt", 'w')
        for line in strong_lines:
            elements = line.split()
            # print elements[0]+'\t'+elements[1]+'\t'+elements[2]
            print >> f_o, elements[0]+'\t'+elements[1]+'\t'+elements[2]
        file.close()
        f_o.close()

if __name__ == "__main__":
    enrichments_old = range(5, 100, 10)
    enrichments = [x/100.0 for x in enrichments_old]
    gen_strong_peaks(sys.argv[1], enrichments)