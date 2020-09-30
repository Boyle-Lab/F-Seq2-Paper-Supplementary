import subprocess

signal_file = '/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/CTCF/BamFiles/ENCFF961BON.bam'
control_file = '/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/CTCF/BamFiles/ENCFF444CLV.bam'

subprocess.run(f"macs2 callpeak -t {signal_file} -c {control_file} -f BAM --outdir ./MACS2_output/ -g hs -B -q 0.05", shell=True)

