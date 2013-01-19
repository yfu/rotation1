#! /usr/bin/python

# This pipeline will
# 1. take a bed file as input.
# 2. generate several bed file according to HOTness
# 3. submit to GREAT and retrieve the results
# 4. parse the results by GREAT and get the q-value
# 5. save the q-value into a file
from gen_hot_bed import gen_hot_bed
from parse_GREAT_output import parse_GREAT_output
from urllib import urlencode
from subprocess import call
import sys


def pipeline(file, column):
    # Step 1
    print "*" * 80
    print "Step 1..."
    f_i = open(sys.argv[1], 'r')
    print "File opened."
    print "Step 1 Done!"
    print "*" * 80
    
    # Step 2
    print "*" * 80
    print "Step 2..."
    hotness_list = range(0, 101, 5)
    # hotness_list = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
    
    ########################################################################################
    # For debugging only                                                                   #
    # hotness_list = [65, 70] # Simple hotness_list to make life (debugging) easier... #
    ########################################################################################
    
    print "I will generate a bed file for each hotness: ",
    print hotness_list
    gen_hot_bed(f_i, hotness_list)
    print "Step 2 Done!"
    print "*" * 80
    
    # Quest Example
    # wget -O results.tsv "http://bejerano.stanford.edu/great/public/cgi-bin/greatStart.php?outputType=batch&requestSpecies=hg18&requestName=Example+Data&requestSender=Client+A&requestURL=http%3A%2F%2Fwww.clientA.com%2Fdata%2Fexample1.bed"
    
    # Step 3
    print "*" * 80
    print 'Step 3...'
    for h in hotness_list:
        fn = 'hot' + str(h) +'.bed'
        print "I am uploading %s" % fn
        
        source_bed = "http://zlab.bu.edu/great/SydhTfbsK562/" + fn
        
        print 
        u = {'outputType':'batch', 'requestSpecies':'hg19', 'requestName':'YuRequests', 'requestSender':'Yu', 'requestURL':source_bed}
        
        source_great = "http://bejerano.stanford.edu/great/public/cgi-bin/greatStart.php?"
        quest = source_great + urlencode(u) # The 'address' part of wget command
        
        great_output_file = 'hot' + str(h) + '.great' + '.tsv'
        command = ['wget', '-O', great_output_file, quest]
        print command
        call(command)
        
    # Step 4
    print "*" * 80
    print "Step 4..."
    print ""
    
    values = []
    
    for h in hotness_list:
        great_output_file = 'hot' + str(h) + '.great' + '.tsv'
        f_i_tsv = open(great_output_file, 'r')
        bed_fn = 'hot' + str(h) + '.bed'
        print "I am processing %s" % bed_fn
        v = parse_GREAT_output(f_i_tsv, "GO:0034728", column)
        f_i_tsv.close()
        values.append(v)
    
    length = len(values)
    
    f_o_parse = open("great_final.txt", 'w')
    
    for i in range(length):
        print >> f_o_parse, str(hotness_list[i]) + '\t' + str(values[i])
    
    print "*" * 80
    
    print "All done!"
        
    
def main():
    f_i = open(sys.argv[1], 'r')
    column = sys.argv[2]
    pipeline(f_i, column) 

if __name__ == '__main__':
    main()
    