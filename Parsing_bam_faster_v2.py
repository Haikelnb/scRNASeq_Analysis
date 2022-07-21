import sys
import re
from collections import defaultdict


output_file_1 = open('/PATH/TO/WORKING/DIRECTORY/Unique_seq_per_droplet_SAMPLE.txt', 'w+')  ### EDIT TO DESIRED PATH AND SAMPLE NAME
output_file_2 = open('/PATH/TO/WORKING/DIRECTORY/Mapped_per_Unique_sequence_SAMPLE.txt', 'w+') ### EDIT TO DESIRED PATH AND SAMPLE NAME

BC_dict = defaultdict(list)
Dupl_counter = defaultdict(int)

for line in sys.stdin:
    read_stats = list(line.split("\t"))
    name = read_stats[0]
    nucleotide_position = read_stats[3]
    chromosome = read_stats[2]
    strand_alignment = read_stats[1]
    if strand_alignment == '16':
        strand_id = 'reverse_strand'
        name_elements = list(name.split("_"))
        BC = name_elements[1]
        UMI = name_elements[2]
        Unique_seq = BC + '\t' + UMI + '\t' + nucleotide_position + '\t' + chromosome + '\t' + strand_id
        if Unique_seq not in BC_dict[BC]:
            BC_dict[BC].append(Unique_seq)
        Dupl_counter[Unique_seq] += 1
    elif strand_alignment == '0':
        strand_id = 'forward_strand'
        name_elements = list(name.split("_"))
        BC = name_elements[1]
        UMI = name_elements[2]
        Unique_seq = BC + '\t' + UMI + '\t' + nucleotide_position + '\t' + chromosome + '\t' + strand_id
        if Unique_seq not in BC_dict[BC]:
            BC_dict[BC].append(Unique_seq)
        Dupl_counter[Unique_seq] += 1

print('10X_Barcode\tUnique_Sequences', file=output_file_1)
for k in BC_dict:
    print(k, '\t', len(BC_dict[k]), file=output_file_1)

print('Unique_sequence\t\t\t\t\t\t\t\tDuplicates', file=output_file_2)
for k in Dupl_counter:
    print(k, '\t', Dupl_counter[k], file=output_file_2)