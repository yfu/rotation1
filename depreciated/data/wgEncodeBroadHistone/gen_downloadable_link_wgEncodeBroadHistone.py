f = open("all_peak_files_wgEncodeBroadHistone.txt", 'r')
f_download_link = open("download.txt", 'w')

prefix = "http://hgdownload-test.cse.ucsc.edu/goldenPath/hg19/encodeDCC/wgEncodeBroadHistone/"

for line in f.xreadlines():
    e = line.split()
    link = prefix + e[0]
    command = 'wget ' + link
    print >> f_download_link, command
f.close()
f_download_link.close()

    