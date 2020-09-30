## Data Details

- Fastq files were downloaded from SRA where accession number = `SRR891268`
- Aligned to hg38 human genome with `bwa-mem`
- Further process to sort by name since bedtools -BEDPE requires that  
`$ samtools sort -n /data/projects/FootPrinting/ATAC-seq/SRR891268.pruned.bam -o /data/data_repo/samzhao/F_seq/ATAC_seq_benchmark/GM12878/BamFiles/SRR891268.pruned.sortByName.bam`
