f = open("peak_files.txt", 'r')
f_download_link = open("peak_file_download_links.txt", 'w')

prefix = "http://hgdownload-test.cse.ucsc.edu/goldenPath/hg19/encodeDCC/wgEncodeSydhTfbs/"

for line in f.xreadlines():
    e = line.split()
    link = prefix + e[0]
    command = 'wget ' + link
    print >> f_download_link, command
f.close()
f_download_link.close()

    