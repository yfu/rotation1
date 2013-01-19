#! /usr/bin/python
# This script will parse the output file (*.tsv) by GREAT batch mode.
# This function will take a file object (the output by GREAT batch mode), term ID (the term you query), column (which column
# in that tsv file you want, e.g. Binomial Raw P-value, Hypergeometric Bonferroni P-value or the 14, 15. You can use either the column number or the 
# column name) as input and returns the specific value you query.

import sys
def parse_GREAT_output(file, iden, column):
    """Parse the output of GREAT batch mode and return the queried value."""
    
    flag_id_found = False # The default value of the varible is false, indicating that the queried id is not found
    # If that id is found, set the flag to true
    
    flag_column_found = False # Indicates whether column is legal.
    value = None
    column = str(column)
    if (column.lower() == "hypergeometric raw p-value") or (column == "13"): 
        # Convert the parameter into lowercase to handle allpossible wrong uppercase or lower-case.
        column = 13 # Obtain Column 13
    elif (column.lower() == "hypergeometric bonferroni p-value") or (column == "14"):
        column = 14
    elif (column.lower() == "binomial raw p-value") or (column == "4"):
        column = 4
    elif (column.lower() == "binomial bonferroni p-value") or (column == "5"):
        column = 5
    else:
        column = int(column)
        print "Are you sure you want to use column %d?" % column
        
    print "You are querying \"%s\" term and I will try to return %s column" % (iden, column)
    print '*' * 80
    
    value = ""
    for line in file.xreadlines():
        if line.startswith('<'):
            print "I cannot find the value you want because GREAT returns nothing. I will return 1"
            value = 1
            break
        line = line.strip()
        
        # print "*" * 10
        # print line
        # print type(line)
        # print "*" * 10
        
        if line == "" or line[0] == '#': # If the line starts with a "#", that means this is just a comment from file. Hence, ignore that line
            continue
        elements = line.split('\t')
        if len(elements) == 0:
            continue
        # print elements
        # print elements[column]
        # print elements
        
        
        if elements[1] == iden:
            flag_id_found = True
            value = elements[column]
    
    
    if value != None and flag_id_found == True:
        print "Result:"
        print "Query is successful!"
        print "Term ID: %s" % iden
        print "Value: %s" % value
    else:
        print "I cannot find the value you want. I will return 1"
        value = 1 
        
        
    return value

def main():
    f_i = open(sys.argv[1], 'r')
    v = parse_GREAT_output(f_i, "GO:0032465", 13)
    
    
if __name__ == "__main__":
    main()

    
            
            