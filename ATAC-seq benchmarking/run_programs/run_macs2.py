import subprocess

signal_file =  '/data/data_repo/samzhao/F_seq/ATAC_seq_benchmark/GM12878/BamFiles/SRR891268.pruned.sortByName.bam'

subprocess.run(f"macs2 callpeak -t {signal_file} --shift -75 --extsize 150 --nomodel -f BAM --outdir ./MACS2_output/ -g hs -B -q 1.0 --keep-dup all --name NA_SE_1", shell=True)
#subprocess.run(f"macs2 callpeak -t {signal_file} -f BAMPE --outdir ./MACS2_output/ -g hs -B -q 1.0", shell=True)
