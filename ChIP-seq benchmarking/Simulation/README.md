## Simulation procedures

- generate fastq files in `FastqFiles`  
run `Rscript GenerateSimulatedDataRed.R`  

- generate bam files  
put genome file under `random_genome`  
```
$ cd random_genome
$ module load BWA
$ bwa index TenMillion_Genome_Enrichment_25.fa
$ cd ..
$ bash generate_bam.sh
```

- peak calling by running scripts in `run_programs`


This was reproduced from [Thomas et al.](https://academic.oup.com/bib/article/18/3/441/2453291).  
The scripts were downloaded from [here](https://gb.ucsf.edu/bio/browser/rthomas/BenchmarkChIPseqPeakCallers_Code/).
