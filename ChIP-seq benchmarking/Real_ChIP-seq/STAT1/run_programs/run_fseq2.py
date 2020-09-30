import subprocess

signal_file = '/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/STAT1/BamFiles/ENCFF895RMY_sortedByName.bam'
control_file = '/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/STAT1/BamFiles/ENCFF941TZZ_sortedByName.bam'

subprocess.run(f"fseq2 callpeak {signal_file} -control_file {control_file} -l 50 -t 8.0 -o ./Fseq2_output -name STAT1 -cpus 4 -v -sig_format bigwig -chrom_size_file ../CTCF/BamFiles/hg19.chrom.sizes", shell=True)

