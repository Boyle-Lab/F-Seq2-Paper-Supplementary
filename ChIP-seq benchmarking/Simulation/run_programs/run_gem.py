import os
import pandas as pd
import pybedtools
import numpy as np
import subprocess
import fnmatch

bam_dir = '/home/samzhao/F_seq/ChIP_seq_benchmark/Simulated_Data/BamFiles/'
for bam_file in os.scandir(bam_dir):
    if fnmatch.fnmatch(bam_file.path, '*_Input_*.bam'):
        control_file = bam_file.path
        file_name_ls = bam_file.path.split('_')
        signal_file = '_'.join(bam_file.path.split('_')[0:-2] + bam_file.path.split('_')[-1:])
        exp_num = bam_file.path.split('_')[-1].split('.')[0]
        name = 'GEM_' + exp_num
        subprocess.run(f"java -Xmx10G -jar /home/samzhao/F_seq/ChIP_seq_benchmark/Simulated_Data/gem/gem.jar prlimit --cpu=30 --q 0 --d /home/samzhao/F_seq/ChIP_seq_benchmark/Simulated_Data/gem/Read_Distribution_default.txt --g /home/samzhao/F_seq/ChIP_seq_benchmark/Simulated_Data/random_genome/Test_TenMillion_Genome.chrom.sizes   --expt {signal_file} --ctrl {control_file} --f BAM  --out ./GEM_output/{name}", shell=True)
