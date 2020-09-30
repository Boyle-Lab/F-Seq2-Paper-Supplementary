import subprocess

signal_file = '/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/CTCF/BamFiles/ENCFF961BON.bam'
control_file = '/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/CTCF/BamFiles/ENCFF444CLV.bam'
name = 'GEM_1'
subprocess.run(f"java -Xmx10G -jar /home/samzhao/F_seq/ChIP_seq_benchmark/Simulated_Data/gem/gem.jar prlimit --cpu=30 --q 2 --d /home/samzhao/F_seq/ChIP_seq_benchmark/Simulated_Data/gem/Read_Distribution_default.txt --g /home/samzhao/F_seq/ChIP_seq_benchmark/Simulated_Data/gem/hg19.chrom.sizes --genome /home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/CTCF/seq_GEM/ --expt {signal_file} --ctrl {control_file} --f BAM --out ./GEM_1_output/{name} --k_min 6 --k_max 13 --smooth 3 --t 8", shell=True)

