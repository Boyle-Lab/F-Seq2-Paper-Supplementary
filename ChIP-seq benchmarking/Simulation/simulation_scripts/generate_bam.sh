sourcedir=/home/samzhao/R/compare_chip_peak_caller/FastqFiles/*fastq* # need to change accordingly
#sourcedir1=/home/samzhao/R/compare_chip_peak_caller/Test/

for f in $sourcedir
do
  fbase=$(basename "$f")
  echo "$f"
  echo "Inside $fbase"

  fsortbase=${fbase/.fastq/}
  fsortbase1="$fsortbase.sam"
  fsortbase2="$fsortbase.bam"
  
  bwa mem -t 20 /home/samzhao/R/compare_chip_peak_caller/random_genome/TenMillion_Genome_Enrichment_25.fa "$f" > /home/samzhao/R/compare_chip_peak_caller/BamFiles/"$fsortbase1"
  samtools view -S -b /home/samzhao/R/compare_chip_peak_caller/BamFiles/"$fsortbase1" > /home/samzhao/R/compare_chip_peak_caller/BamFiles/"$fsortbase2"
  rm /home/samzhao/R/compare_chip_peak_caller/BamFiles/"$fsortbase1"
  
done

