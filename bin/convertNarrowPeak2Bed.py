#!/usr/bin/python
# Convert narrowPeak files to bed files
# Since narrpwPeak files use different format (the 4th column and later),
# this script will delete 4th, 5th, 6th ... columns

def convertNarrowPeak2Bed(file):
    new_line = []
    for line in file.xreadlines():
        elements = line.split()
        chr = elements[0]
        start = elements[1]
        end = elements[2]
        new_line.append(chr+'\t'+start+'\t'+end)
        
    return new_line

def main():
    import sys, os
    
    if len(sys.argv) !=2:
        print "Usage: %s input_file_name" % sys.argv[0]
        sys.exit(1)
    f_i = open(sys.argv[1], 'r')
    
    filename, _ = os.path.splitext(sys.argv[1])
    
    f_o = open('./bed/'+filename+'.bed', 'w')
    # print './bed/'+filename+'.bed'
    
    new_lines = convertNarrowPeak2Bed(f_i)
    
    for line in new_lines:
        print >> f_o, line
    # print './bed/'+sys.argv[1]
    print "I will save the bed files in ./bed directory."
    
if __name__ == "__main__":
    main()