#!/usr/bin/python

# This script can take a bed file (containing several bed files from ChIP-seq experiment in the same cell line but different TFs)
# and generate a series of bed files that have different HOTness, like 5, 10, 15, 20, 25, 30, 35, 40, 45 ...

def gen_hot_bed(file, hotnesses):
    """ Take a file object and generate a series of bed files that have different HOTness. HOTness is specified by the second 
parameter. The second parameter should be a list which contains the hotnesses one want, like [5, 8, 10, 15, 20, 25, 30, 35, 40]
    """
    features = [] # Save each line and its hotness as a tuple, like ("chr1  138811  139312  1", 1)
    for line in file.xreadlines():
        # print line 
        elements = line.split()
        chrom = elements[0]
        start = elements[1]
        end = elements[2]
        hotness = elements[3]
        features.append((line, int(hotness))) # Like this: ("chr1  138811  139312  1", 1)
    
    for h in hotnesses: # HOTnesses specified by the user
        print "HOTness: %d" % h
        fn = "hot"+str(h)+'.bed'
        f_o = open(fn, 'w')
        print "I will save the file as %s" % fn
        for l, hotness in features: # hotness here is unpacked from one element of feature
            if hotness >= h:
                print >> f_o, l,
        print "Finished! Please check file %s" % fn
    
def main():
    import sys
    f_i = open(sys.argv[1], 'r')
    
    # hotness_list = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
    hotness_list = range(1, 70)
    print "I will generate a bed file for each hotness: ",
    print hotness_list
    gen_hot_bed(f_i, hotness_list)
    print "Done!"

if __name__ == "__main__":
    main()
            
        
        
        
