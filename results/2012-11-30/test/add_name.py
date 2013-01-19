import glob, os, re

def add_name(filename):
    f = open(filename, 'r')
    f_out = open("./output/"+filename, 'w')
    for line in f.xreadlines():
        ele = line.split()
        ele[3] = filename[:-18]
        
        for e in ele:
            print >> f_out, e+'\t',
            # print e+'\t',
        print >> f_out, '\n',
        # print '\n'
    f.close()
    f_out.close()





all_filenames = os.listdir(os.getcwd())
for f in all_filenames:
    if ".narrowPeak" in f:
        add_name(f)


