# This script will generate the distribution of the number of Histones in each genomic location.
# For example:
# =========  =======  ===== =====
#  A B C D     D  E    F     G H
# Ditribution would be:
# Number of histones (or other elements) each region has | Number of such regions
# 4 1
# 2 2
# 1 1



def sim_stat(filename):
    di = dict()
    
    f = open(filename, 'r')
    for line in f.xreadlines():
        ele = line.split()
        el = len(ele[3].split(';'))
        try:
            di[el] += 1
        except Exception, e:
            print "This is the first time that I add a region containing %d peaks."%el
            di[el] = 1
    return di

def main():
    import sys
    if len(sys.argv)!=2:
        print "Usage: python %s input_file_name"%sys.argv[0]
        exit(-1)
    
    filename = sys.argv[1]
    f_out = open("simple_statistics.txt", 'w')
    d = sim_stat(filename)
    for key in d.keys():
        print "%d genomic regions have %d peaks."%(d[key], key)
        # print >> f_out, str(key) + '\t' + str(d[key])
        num_of_peaks = key
        num_of_regions = d[key]
        for i in range(num_of_regions):
                    print >> f_out, num_of_peaks
    f_out.close()
if __name__ == '__main__':
    main()