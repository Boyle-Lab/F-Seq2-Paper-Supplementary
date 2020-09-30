import subprocess

signal_file = '/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/STAT1/BamFiles/ENCFF895RMY.bam'
control_file = '/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/STAT1/BamFiles/ENCFF941TZZ.bam'

subprocess.run(f"macs2 callpeak -t {signal_file} -c {control_file} -f BAMPE --outdir ./MACS2_output/ -g hs -B -q 0.05", shell=True)

