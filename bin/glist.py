def glist(f):
    names = []
    
    l = f.readlines()
    
    l = l[0]
    ele = l.split('\r')
    for e in ele:
        n = e.split('|')
        for name in n:
            names.append(name)
    
    return names


if __name__ == "__main__":
    f = open("gene_list.txt", 'r')
    out_f = open("gene_list_new", 'w')
    result = glist(f)
    # print result
    for i in result:
        print >> out_f, i
    f.close()
    out_f.close()
    # print result