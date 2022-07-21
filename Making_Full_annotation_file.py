import re

gff_filepath = '/PATH/TO/GFF/FILE/gff_file.gff'     ### EDIT TO DESIRED PATH AND GFF FILE NAME

output_file = open('/PATH/TO/WORKING/DIRECTORY/Full_annotation_filename.txt', 'w+')     ### EDIT TO DESIRED PATH AND ANNOTATION FILE NAME

with open(gff_filepath) as fp1:
    for gff_line in fp1:
        if re.match('^#', gff_line):
            next
        else:
            annot_stats = list(gff_line.split("\t"))
            gene_stats = annot_stats[2]
            Chromosome = annot_stats[0]
            if gene_stats == "mRNA":
                gene_start = int(annot_stats[3])
                gene_end = int(annot_stats[4])
                strand = annot_stats[6]
                gene_info = list(annot_stats[8].split("="))
                gene_ID_stats = list(gene_info[2].split(";"))
                gene_ID_Only = gene_ID_stats[0].strip("gene-")
                if strand == "+":
                    strand_name = "forward_strand"
                else:
                    strand_name = "reverse_strand"
                if re.findall('product', gff_line):
                    Protein_info = list(annot_stats[8].split("product="))
                    ProteinName_stats = list(Protein_info[1].split(";"))
                    ProteinName_Only = ProteinName_stats[0]
                    ProteinName_Only = ProteinName_Only.replace(" ", "_")
                    Gene_full_name = (gene_ID_Only + '_' + ProteinName_Only)
                    print(Chromosome, "\t", Gene_full_name, "\t", gene_start, "-", gene_end, "\t", strand_name, file=output_file)
                else:
                    Gene_full_name = gene_ID_Only
                    print(Chromosome, "\t", Gene_full_name, "\t", gene_start, "-", gene_end, "\t", strand_name, file=output_file)

