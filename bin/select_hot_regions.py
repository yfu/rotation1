#!/usr/bin/python
# This script will select those regions whose HOTness is >= n

import sys

# It takes two parameters - filename and n

if len(sys.argv) != 4:
    print "Usage: %s n input output" % sys.argv[0]
    sys.exit()

f_i = open(sys.argv[2], 'r')
f_o = open(sys.argv[3], 'w')
n = int(sys.argv[1])

for line in f_i.xreadlines():
    elements = line.split()
    hotness = int(elements[3])
    if hotness >= n:
        print >> f_o, line,
