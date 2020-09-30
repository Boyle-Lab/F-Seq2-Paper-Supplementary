import subprocess

signal_file = '/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/STAT1/BamFiles/ENCFF895RMY.bam'
control_file = '/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/STAT1/BamFiles/ENCFF941TZZ.bam'

subprocess.run(f"samtools view {signal_file} | /home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/SPI1/PeakSeq/bin/PeakSeq -preprocess SAM stdin ./PEAKSEQ_output/treatment", shell=True)

subprocess.run(f"samtools view {control_file} | /home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/SPI1/PeakSeq/bin/PeakSeq -preprocess SAM stdin ./PEAKSEQ_output/control", shell=True)

subprocess.run(f"/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/SPI1/PeakSeq/bin/PeakSeq -peak_select /home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/STAT1/PEAKSEQ_output/config.dat", shell=True) #change config.dat accordingly
