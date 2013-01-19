import os
from subprocess import call
all_filenames = os.listdir(os.getcwd())

peak_filenames = []
for n in all_filenames:
    if ("Peak" in n) and (".gz" not in n):
        peak_filenames.append(n)
print peak_filenames

for n in peak_filenames:
    print n
    # call(["python", "./peak2gene.py"])
    
    command = "./peak2gene.py" + " --name=" + n + " --op=all"+\
    " --distance=2000" + " --genome=./hg19.refGene"+ " --treat=./"+n
    print command
    call(['python', 'peak2gene.py', '--name='+n, '--op=all', '--distance=2000', '--genome=./hg19.refGene', '--treat=./'+n])
