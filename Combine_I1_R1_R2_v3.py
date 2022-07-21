## This script takes in the sample barcode, R1, and R2, fastq files and parses read belonging to each sample

import sys
import re
from itertools import islice
import gzip


I1_filepath = sys.argv[1]
R1_filepath = sys.argv[2]
R2_filepath = sys.argv[3]


output_file = gzip.open('/PATH/TO/WORKING/DIRECTORY/SAMPLE_Matched_reads.fastq.gz', 'wt')  ### EDIT TO DESIRED PATH AND SAMPLE NAME

Barcodes_list = ['TACCACCA', 'CTAAGTTT', 'GGGTCAAG', 'ACTGTGGC']  # input 4 sample indexing barcodes


with gzip.open(I1_filepath, mode='rt') as fp1:  # the rt mode is for reading gzipped or binary files as text
    with gzip.open(R1_filepath, mode='rt') as fp2:
        with gzip.open(R2_filepath, mode='rt') as fp3:
            # line = fp1.readline()
            Total_reads_count = 0
            Total_matched_seq = 0
            Trimmed_seq_count = 0
            for I1_line in fp1:
                # print(line, end='')
                if re.match('^@', I1_line):
                    Total_reads_count += 1
                    I1_header = list(I1_line.split(" "))
                    # print(I1_header[0])
                    all_names = I1_header[0]
                if I1_line.strip() in Barcodes_list:
                    matched_name = all_names
                    # print(matched_name)
                    for R1_line in fp2:
                        # print(matched_name)
                        #Total_matched_seq += 1
                        if re.search(matched_name, R1_line):
                            # print(matched_name, R1_line)
                            R1_seq = next(fp2, '').strip()
                            BC = R1_seq[0:15]
                            UMI = R1_seq[16:25]
                            break

                    for R2_line in fp3:

                        if re.search(matched_name, R2_line):
                            # print(matched_name, R2_line,)
                            Total_matched_seq += 1
                            mRNA = list(islice(fp3, 1))[-1]
                            Quality = list(islice(fp3, 2))[-1]
                            #print(mRNA)
                            x = mRNA.find('AAAAAA')
                            if x == (-1):
                                print(matched_name+'_'+BC+'_'+UMI, file=output_file)
                                print(mRNA, end='', file=output_file)
                                print('+', file=output_file)
                                print(Quality, end='', file=output_file)
                                break
                            else:
                                Trimmed_seq_count += 1
                                trimming_end = (x - 1)
                                #print(mRNA, x, trimming_end)
                                trimmed_seq = mRNA[0:trimming_end]
                                trimmed_quality = Quality[0:trimming_end]
                                print(matched_name+'_'+BC+'_'+UMI, file=output_file)
                                print(trimmed_seq, file=output_file)
                                print('+', file=output_file)
                                print(trimmed_quality, file=output_file)
                                break
print('Total reads:', Total_reads_count, '  # of matched sequences:', Total_matched_seq, '  # of trimmed sequences:', Trimmed_seq_count)