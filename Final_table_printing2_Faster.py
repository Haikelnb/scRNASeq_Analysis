import re
from collections import defaultdict
from collections import Counter

annotation_filepath = '/PATH/TO/ANNOTATION/FILE/annotation_file_name.txt'        ### EDIT TO DESIRED PATH AND ANNOTATION FILE NAME
Mapped_filepath = '/PATH/TO/WORKING/DIRECTORY/Mapped_per_Unique_sequence_Saliva_Sachie1_ReRun.txt'       ### EDIT TO DESIRED PATH AND SAMPLE NAME
UniqSeq_filepath = '/PATH/TO/WORKING/DIRECTORY/Mapped_per_Unique_sequence_SAMPLE.txt'        ### EDIT TO DESIRED PATH AND SAMPLE NAME

output_file = open('/PATH/TO/WORKING/DIRECTORY/Final_hits_SAMPLE.txt', 'w+')         ### EDIT TO DESIRED PATH AND SAMPLE NAME

Hits_dict = defaultdict(list)
Annot_dict = defaultdict(dict)

BC_list = []
with open(UniqSeq_filepath) as fp3:
    for uniqseq_line in fp3:
        if re.match('10X_Barcode', uniqseq_line):
            next
        else:
            barcode_line = list(uniqseq_line.split("\t"))
            number_uniqseq = int(barcode_line[1])
            uniq_barcode = barcode_line[0]
            uniq_barcode = uniq_barcode.strip()
            if (250 <= number_uniqseq <= 5000):  ###### This needs user input: depending on the data select the # of unique sequences of cells for downstream analysis;
                BC_list.append(uniq_barcode)        

with open(annotation_filepath) as fp1:
    for annot_line in fp1:
        annot_stats = list(annot_line.split("\t"))
        gene_name = annot_stats[1]
        gene_range = annot_stats[2]
        chromosome = annot_stats[0].strip()
        gene_position = list(gene_range.split("-"))
        start = int(gene_position[0])
        end = int(gene_position[1])
        positions = range(start-1, end+1, 1)
        Annot_dict[chromosome].update({positions: gene_name})

#for K1, V1 in Annot_dict.items():
#    print(K1, '\t')
#    for K2, V2 in V1.items():
#        print(K2, V2)


with open(Mapped_filepath) as fp2:
    for mapped_line in fp2:
        if re.match('Unique_sequence', mapped_line):
            next
        else:
            unique_line = list(mapped_line.split("\t"))
            base = int(unique_line[2])
            mapped_chr = unique_line[3].strip()
            Barcode = unique_line[0]
            for K1, V1 in Annot_dict.items():
                if (K1 == mapped_chr):
                    for K2, V2 in V1.items():
                        if (base in K2):
                            Hits_dict[V2].append(Barcode)

for i in BC_list:
    print('\t', i.strip(), end='', file=output_file)

for l in sorted(Hits_dict):
    counts = Counter(Hits_dict[l])
    l = l.strip()
    print('\n',l, end='\t', file=output_file)
    for i in BC_list:
        for j, k in counts.items():
            if i in j:
                count = k
                break
            else:
                count = 0
        print(count, end='\t', file=output_file)



