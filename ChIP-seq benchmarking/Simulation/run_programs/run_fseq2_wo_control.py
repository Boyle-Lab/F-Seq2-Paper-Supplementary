import os
import pandas as pd
import pybedtools
import numpy as np
import subprocess
import fnmatch
import multiprocessing as mp

bam_dir = '/home/samzhao/F_seq/ChIP_seq_benchmark/Simulated_Data/BamFiles/'
input_param_ls = []
cpus = 20
def run_program(signal_file, name):
    subprocess.run(f"fseq2 callpeak {signal_file} -l 50 -t 8.0 -f 166 -p_thr False -o ./Fseq2_output_wo_control -name {name} -sparse_data -cpus 1 -v", shell=True)
    return

for bam_file in os.scandir(bam_dir):
    if fnmatch.fnmatch(bam_file.path, '*_Input_*.bam'):
        control_file = bam_file.path
        file_name_ls = bam_file.path.split('_')
        signal_file = '_'.join(bam_file.path.split('_')[0:-2] + bam_file.path.split('_')[-1:])
        exp_num = bam_file.path.split('_')[-1].split('.')[0]
        name = 'Fseq2_' + exp_num
        input_param_ls.append([signal_file, name])

with mp.Pool(processes=cpus) as pool:
    results = pool.starmap(run_program, input_param_ls)
