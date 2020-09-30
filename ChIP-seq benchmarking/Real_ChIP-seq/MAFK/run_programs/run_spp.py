import subprocess

signal_file = '/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/MAFK/BamFiles/ENCFF251HGY.bam'
control_file = '/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/MAFK/BamFiles/ENCFF107SKX.bam'

subprocess.run(f"Rscript /home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/SPI1/phantompeakqualtools/run_spp.R -c={signal_file} -i={control_file} -p=10 -fdr=1.0 -odir=./SPP_output/ -savn -savr", shell=True)
