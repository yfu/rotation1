All bed (narrowPeak) files are processed using GREAT

Then the GREAT results are parsed to contain only the binom and hyper p-values and their corresponding GO terms.

top1000_common_terms.txt contains the most frequent GO terms.

gen_tab.pl can utilize those GO terms and generate a table in which, one row represents a TF and columns represent Ontology, ID, binom p-value and hyper p-value.

