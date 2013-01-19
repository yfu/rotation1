# This script will resize the regions in a bed file to a unified size that the user specify.
# It will extend the middle point by the "size" parameter.
# e.g. If the user specifies size to be 5, then the result region will be:
# -----M-----

import sys, os

def resize(file, size):
    size = int(size)
    counter = 0
    lines = []
    for line in file.xreadlines():
        counter += 1
        elements = line.split()
        # Since bed files use 0-based coordinates and the end position is excluded,
        # the actual start position is the 2nd column and the actual end position is
        # the 3rd column - 1. Hence, the middle point is (2nd + 3rd - 1) / 2. And based on
        # this value, extend the middle point up-/down-stream by size/2.
        start = int(elements[1])
        end = int(elements[2])
        mid = (start + end - 1) / 2
        new_start = mid - size
        assert(new_start>0)
        new_end = mid + size + 1 # Because bed files are 0-based, I need to add extra 1 here.
        
        new_line = elements[0] +'\t' + str(new_start) + '\t' + str(new_end) + '\t' + elements[3] + \
        '\t' + elements[4] + '\t' + elements[5] + '\t' + elements[6] + '\t' + elements[7] + '\t' + \
        elements[8] + '\t' + elements[9]
        lines.append(new_line)
    return lines

def main():
    msg = """cd to your directory containing the bedfiles first
Usage: python %s bedfile up/downstream_size"""
    if len(sys.argv) != 3:
        print msg
        sys.exit(1)
    f_i = open(sys.argv[1], 'r')
    lines = resize(f_i, sys.argv[2])
    cwd = os.getcwd()
    filename, ext = os.path.splitext(sys.argv[1])
    
    output_name = filename + "Resized" + sys.argv[2] + ext
    f_o = open(output_name, 'w')
    for line in lines:
        print >> f_o, line

if __name__ == "__main__":
    main()
    
    
    
    
    
    

        