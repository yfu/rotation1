#!python

# This script will find the strong peaks by percentage.
# For example, if percentage is set to 80%, then, those peak whose strenth rank top 80% 
# will be the output.
from subprocess import call
import sys
from suds.client import Client
import os


def DAVIDenrich(listF, idType, bgF='', resF='', bgName = 'Background1',listName='List1', category = '', thd=0.1, ct=2):

   
    if len(listF) > 0 and os.path.exists(listF):
        inputListIds = ','.join(open(listF).read().split('\n'))
        print 'List loaded.'        
    else:
        print 'No list loaded.'
        raise

    flagBg = False
    if len(bgF) > 0 and os.path.exists(bgF):
        inputBgIds = ','.join(open(bgF).read().split('\n'))
        flagBg = True
        print 'Use file background.'
    else:
        print 'Use default background.'

    client = Client('http://david.abcc.ncifcrf.gov/webservice/services/DAVIDWebService?wsdl')
    print 'User Authentication:',client.service.authenticate('yfu@bu.edu')

    listType = 0
    print 'Percentage mapped(list):', client.service.addList(inputListIds,idType,listName,listType)
    if flagBg:
        listType = 1
        print 'Percentage mapped(background):', client.service.addList(inputBgIds,idType,bgName,listType)

    print 'Use categories:', client.service.setCategories(category)
    chartReport = client.service.getChartReport(thd,ct)
    chartRow = len(chartReport)
    print 'Total chart records:',chartRow
    
    if len(resF) == 0 or not os.path.exists(resF):
        if flagBg:
            resF = listF + '.withBG.chartReport'
        else:
            resF = listF + '.chartReport'
    with open(resF, 'w') as fOut:
        fOut.write('Category\tTerm\tCount\t%\tPvalue\tGenes\tList Total\tPop Hits\tPop Total\tFold Enrichment\tBonferroni\tBenjamini\tFDR\n')
        for row in chartReport:
            rowDict = dict(row)
            categoryName = str(rowDict['categoryName'])
            termName = str(rowDict['termName'])
            listHits = str(rowDict['listHits'])
            percent = str(rowDict['percent'])
            ease = str(rowDict['ease'])
            Genes = str(rowDict['geneIds'])
            listTotals = str(rowDict['listTotals'])
            popHits = str(rowDict['popHits'])
            popTotals = str(rowDict['popTotals'])
            foldEnrichment = str(rowDict['foldEnrichment'])
            bonferroni = str(rowDict['bonferroni'])
            benjamini = str(rowDict['benjamini'])
            FDR = str(rowDict['afdr'])
            rowList = [categoryName,termName,listHits,percent,ease,Genes,listTotals,popHits,popTotals,foldEnrichment,bonferroni,benjamini,FDR]
            fOut.write('\t'.join(rowList)+'\n')
        print 'write file:', resF, 'finished!'
    
    #########################
    # I added the following part
    return chartRow


    


        



def find_strong_peak(file, perc):
    dic = {} # line as the key, strength as the value
    for line in file.xreadlines():
        elements = line.split()
        strength = float(elements[6])
        # print strength
        dic[line] = strength
    
    sorted_lines = sorted(dic.keys(), key=lambda x: -dic[x])
    length = len(sorted_lines)
    return sorted_lines[:int(length*perc)]

def main():
    filename = sys.argv[1]
    
    survival_david = {}
    
    for cutoff in [x/100.0 for x in range(5,101,20)]:
        # Generate a sequence of 0.05, 0.1, 0.15, 0.2, 0.25
        # You can change the step to generate different gredients.
        print "Use the strongest %f%% peaks" % (cutoff*100)
        file = open(sys.argv[1], 'rU')
        strong_lines = find_strong_peak(file, cutoff)
        # print strong_lines
        f_o = open("temp.txt", 'w')
        for line in strong_lines:
            print >> f_o, line,
        file.close()
        f_o.close()
        call(["peak2gene/peak2gene_output_gene_only.py", "-t", "temp.txt", "-n", "test.txt", "--op=all", "-d", "2000", "-g", "peak2gene/hg19.refGene"])
    
        f_glist = open("temp_glist.txt", "r")
        term_num = DAVIDenrich(listF = './temp_glist.txt', idType = 'REFSEQ_MRNA', listName = 'list1', category = 'GOTERM_BP_FAT,GOTERM_CC_FAT,GOTERM_MF_FAT')
        print "David generates %d GO TERMS." % term_num
        survival_david[cutoff] = term_num
    print "*" * 50
    print survival_david
    print "*" * 50
    
    
    

    

if __name__ == "__main__":
    main()