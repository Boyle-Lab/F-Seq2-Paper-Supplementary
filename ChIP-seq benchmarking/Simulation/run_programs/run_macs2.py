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
        name = 'MACS2_' + exp_num
        subprocess.run(f"macs2 callpeak -t {signal_file}  -c {control_file}  -f BAM  -n {name} --outdir ./MACS2_output/  -g 1e7 -B  -q 0.99 --nomodel --extsize 150", shell=True)
