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
        name = 'MUSIC_' + exp_num
        subprocess.run(f'mkdir MUSIC_output_wo_control/{name}',shell=True)
        #subprocess.run(f'mkdir MUSIC_output/{name}/Ipreprocessed', shell=True)
        #subprocess.run(f'mkdir MUSIC_output/{name}/Ipruned', shell=True)
        #subprocess.run(f'mkdir MUSIC_output/{name}/Isorted', shell=True)
        #subprocess.run(f"run_MUSIC.csh -preprocess {control_file} ./MUSIC_output/{name}/Ipreprocessed", shell=True)
        #subprocess.run(f"run_MUSIC.csh -remove_duplicates ./MUSIC_output/{name}/Ipreprocessed ./MUSIC_output/{name}/Isorted ./MUSIC_output/{name}/Ipruned", shell=True)
        
        subprocess.run(f'mkdir MUSIC_output_wo_control/{name}/Cpreprocessed', shell=True)
        subprocess.run(f'mkdir MUSIC_output_wo_control/{name}/Cpruned', shell=True)
        subprocess.run(f'mkdir MUSIC_output_wo_control/{name}/Csorted', shell=True)
        subprocess.run(f"run_MUSIC.csh -preprocess {signal_file} ./MUSIC_output_wo_control/{name}/Cpreprocessed", shell=True)
        subprocess.run(f"run_MUSIC.csh -remove_duplicates ./MUSIC_output_wo_control/{name}/Cpreprocessed ./MUSIC_output_wo_control/{name}/Csorted ./MUSIC_output_wo_control/{name}/Cpruned", shell=True)
        
        subprocess.run(f"MUSIC -get_TF_peaks -begin_l 100 -end_l 200 -l_p 500 -step 1.5 -gamma 4 -chip ./MUSIC_output/{name}/Cpruned -q_val 0.99 -l_mapp 50 -mapp /home/samzhao/F_seq/ChIP_seq_benchmark/Simulated_Data/random_genome", shell=True)
        subprocess.run(f"mv ERs_100.0_200.0_1.50_500_4.0.bed ./MUSIC_output_wo_control/peaks/{name}.peaks", shell=True)
        
