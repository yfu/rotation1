import glob, os, re

def rename(dir, pattern, titlePattern):
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        p = re.compile(r'Uw\w*\.')
        m = p.findall(title)
        print m
        if m!=[]:
            title = m[0][:-1]
            print "!!",title
        os.rename(pathAndFilename, 
                  os.path.join(dir, titlePattern % title + ext))


rename(r'/Users/yfu/Dropbox/Courses/Rotation/idrOptimalBlackListFilt/Bakup', r'*.narrowPeak', r'%s')