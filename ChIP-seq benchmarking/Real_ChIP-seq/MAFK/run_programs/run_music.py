import subprocess

signal_file = '/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/MAFK/BamFiles/ENCFF251HGY.bam'
control_file = '/home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/MAFK/BamFiles/ENCFF107SKX.bam'
name = 'MUSIC_0'

subprocess.run(f'mkdir MUSIC_output/{name}',shell=True)
subprocess.run(f'mkdir MUSIC_output/{name}/Ipreprocessed', shell=True)
subprocess.run(f'mkdir MUSIC_output/{name}/Ipruned', shell=True)
subprocess.run(f'mkdir MUSIC_output/{name}/Isorted', shell=True)
subprocess.run(f"run_MUSIC.csh -preprocess {control_file} ./MUSIC_output/{name}/Ipreprocessed", shell=True)
subprocess.run(f"run_MUSIC.csh -remove_duplicates ./MUSIC_output/{name}/Ipreprocessed ./MUSIC_output/{name}/Isorted ./MUSIC_output/{name}/Ipruned", shell=True)

subprocess.run(f'mkdir MUSIC_output/{name}/Cpreprocessed', shell=True)
subprocess.run(f'mkdir MUSIC_output/{name}/Cpruned', shell=True)
subprocess.run(f'mkdir MUSIC_output/{name}/Csorted', shell=True)
subprocess.run(f"run_MUSIC.csh -preprocess {signal_file} ./MUSIC_output/{name}/Cpreprocessed", shell=True)
subprocess.run(f"run_MUSIC.csh -remove_duplicates ./MUSIC_output/{name}/Cpreprocessed ./MUSIC_output/{name}/Csorted ./MUSIC_output/{name}/Cpruned", shell=True)

subprocess.run(f"MUSIC -get_TF_peaks -begin_l 50 -end_l 200  -l_p 500 -l_win_min 49 -l_win_max 4999 -chip ./MUSIC_output/{name}/Cpruned -control ./MUSIC_output/{name}/Ipruned -q_val 0.05 -l_mapp 50 -mapp /home/samzhao/F_seq/ChIP_seq_benchmark/TF_ChIP_Data/CTCF/mappability_MUSIC/hg19_50bp", shell=True)
subprocess.run(f"mv ERs_50.0_200.0_1.50_500_4.0.bed ./MUSIC_output/peaks/{name}.peaks", shell=True)

