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
        name = 'SPP_' + exp_num
        subprocess.run(f"Rscript /home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/SPI1/phantompeakqualtools/run_spp.R -c={signal_file} -i={control_file} -p=10 -fdr=1.0 -odir=./SPP_output/ -savn=./SPP_output/{name}.narrowpeak -savr=./SPP_output/{name}.regionpeak", shell=True)
