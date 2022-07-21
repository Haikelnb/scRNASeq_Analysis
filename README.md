# scRNASeq_Analysis

The purpose of the following scripts is to output a count table when starting with raw reads of 10x 3’ single cell RNA-Seq data. Each step and how to run each script is explained below. 

1: Combine fastq file information: For each sample/library identified using the I1 reads, get the 10x barcode and UMI sequences from the R1 reads, and cDNA fragment from R1 reads (as well as the Quality sequences) for reads with the same header. This new file is written in a new fastq file as well summary statistics written into a log file

Usage: 
python Combine_I1_R1_R2.py “FastqFileName_I1_001.fastq.gz" “SampleName_R1_001.fastq.gz" “FastqFileName_R2_001.fastq.gz" > SampleName _stats.txt


2: The fastq file generated for each sample is then mapped to the user genome using a mapping software of your preference (e.g., hisat2/STAR)


3: The sam file generated after mapping is converted to a bam file then parsed using the following script. The script parses through the bam file using a samtools view pipe.

Usage: 
•	hisat2 -x indexed genome - S SampleName _R1_001.fastq.gz -S SampleName.sam --no-unal -p (user input)--max-intronlen (user input) &> SampleName _log.txt
•	samtools view -b -S -o SampleName.bam SampleName.sam
•	samtools view SampleName.bam | python Parsing_bam_faster_v2.py


4: In this step, an annotation file is generated from a gff file for the genome used to map the reads above.

Usage:
python Making_Full_annotation_file.py


5: This final step makes a count matrix (gene x cells) for each sample. This can be used for input for downstream scRNA-Seq analysis using R packages. This script needs the outputs from step 3 (“Mapped_per_sequence” and “Unique_seq_per_droplet” files) and annotation file generated from step 4.

Usage: 
python Final_table_printing2.py
