f = open("files.txt", "r")
f_output = open("peak_files.txt", "w")


for line in f.xreadlines():
    e = line.split()
    if "Peak" in e[0]:
        print >> f_output, line,
        # print line

f.close()
f_output.close()