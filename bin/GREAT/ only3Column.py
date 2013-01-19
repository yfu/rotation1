import gzip

def get_3_column(file, dst):
    # Parse the file named "file" and then save it to "dst" directory with the same name.
    print file
    if (".gz" in file):
        f_in = gzip.open(file, 'r')
    else:
        f_in = open(file, 'r')
    f_out = open(dst+'/'+file, 'w')
    
    for line in f_in.readlines():
        chr_num = line[0]
        strt = line[1]
        stp = line[2]
        
        print >> f_out, chr_num + '\t' + strt + '\t' + stp + '\t' + '\r\n'
    f_in.close()
    f_out.close()

if __name__ == "__main__":
    import os
    import sys
    if len(sys.argv) < 3:
        print "Usage: %s source_folder destination_folder"%sys.argv[0]
        sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2]
    all_filenames = os.listdir(src)

    # peak_filenames = []
    num_files = 0
    for n in all_filenames:
        if ("narrowPeak" in n):
            print "File location:", src+n
            get_3_column(src + n, dst)      
            # peak_filenames.append(n)
            num_files += 1
        else:
            print "I cannot process this file %s!"%n
    print "The total number of files:", str(num_files)
    
            