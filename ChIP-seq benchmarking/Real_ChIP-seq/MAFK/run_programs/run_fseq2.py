import subprocess

signal_file = '/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/MAFK/BamFiles/ENCFF251HGY.bam'
control_file = '/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/MAFK/BamFiles/ENCFF107SKX.bam'


subprocess.run(f"fseq2 callpeak {signal_file} -control_file {control_file} -chrom_size_file /home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/CTCF/BamFiles/hg19.chrom.sizes -l 50 -t 8.0 -o ./Fseq2_output -name MAFK -cpus 4 -v -p_thr False", shell=True)
