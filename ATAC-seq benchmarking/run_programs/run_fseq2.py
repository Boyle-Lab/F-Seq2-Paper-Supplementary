import subprocess

signal_file =  '/data/data_repo/samzhao/F_seq/ATAC_seq_benchmark/GM12878/BamFiles/SRR891268.pruned.sortByName.bed'

#subprocess.run(f"fseq2 callpeak {signal_file} -f 0 -l 600 -t 4.0 -o ./Fseq2_output -name GM12878_SE -cpus 6 -v -chrom_size_file ./BamFiles/hg19.chrom.sizes -p_thr False", shell=True)
#subprocess.run(f"fseq2 callpeak {signal_file} -pe -f 0 -l 600 -t 4.0 -o ./Fseq2_output -name GM12878_PE_woFilter -cpus 6 -v -chrom_size_file ./BamFiles/hg19.chrom.sizes -p_thr False", shell=True)
subprocess.run(f"fseq2 callpeak {signal_file} -pe -f 0 -l 600 -t 4.0 -o ./Fseq2_output -name GM12878_PE_auto -cpus 6 -v -chrom_size_file ./BamFiles/hg19.chrom.sizes -pe_fragment_size_range auto -p_thr False", shell=True)
