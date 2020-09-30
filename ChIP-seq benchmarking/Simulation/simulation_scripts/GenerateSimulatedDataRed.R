rm(list=ls())
require('ChIPsim')
require('snowfall')
require('rlecuyer')
sfInit(parallel=TRUE, cpus=20)

#Number of experiments
Nexp <- 100

# enrichment = noise level, set as medium 25
#Fast_FileName <- "/home/rthomas/ChipSeqChallenge/SimulateData/RandomGenome2/FastqFiles/Test_TenMillion_Genome_Enrichment_5_"
#Feat_FileName <- "/home/rthomas/ChipSeqChallenge/SimulateData/RandomGenome2/FeatureFiles/Features_Test_TenMillion_Genome_Enrichment_5_"
Fast_FileName <- "./FastqFiles/Test_TenMillion_Genome_Enrichment_25_"
Feat_FileName <- "./FeatureFiles/Features_Test_TenMillion_Genome_Enrichment_25_"
FileName <- "TenMillion_Genome_Enrichment_25"

#Parameters to play around with
#Transition probabilities
#Gamma distribution
#Enrichment over background
#Pareto distribution parameter
shape1 <- 1
scale1 <- 20
enrichment1 <- 25 #change
r1 <- 2
BindLength <- 50
MinLength <- 150
MaxLength <- 250
MeanLength <- 200
BindingProb <- 0.006
BackgroundProb <- 1-BindingProb
BackgroundFeatureLength <- 1000
BindingFeatureLength <- 500
seed1 <- 1234
seed2 <- 1235
#Number of reads 
Nreads <- 1e5
#length of reads 
LengthReads <- 50
#generate random genome
set.seed(seed1)
chrLen <- c(10e6)
chromosomes <- sapply(chrLen, function(n) paste(sample(c("A", "C", "G", "T"), n, replace = TRUE), collapse = ""))
names(chromosomes) <- paste("CHR", seq_along(chromosomes), sep="")
genome <- DNAStringSet(chromosomes)
chromosomes <- DNAString(chromosomes)
Biostrings::writeXStringSet(genome, file=paste(FileName, ".fa", sep=""), "fasta", width=80, append=FALSE, compress=FALSE, compression_level=NA)


#randomly generate quality of reads
randomQuality <- function(read, ...){
  paste(sample(unlist(strsplit(rawToChar(as.raw(33:126)),"")),
               length(read), replace = TRUE), collapse="")
}

defaultErrorProb1 <- function () 
{
  prob <- list(A = c(1,0,0,0), C = c(0,1,0,0), G = c(0,0,1,0), T = c(0,0,0,1))
  prob <- lapply(prob, "names<-", c("A", "C", "G", "T"))
  prob
}

readError1 <- function (read, qual, alphabet = c("A", "C", "G", "T"), prob = defaultErrorProb1(), 
          ...) 
{
  read <- gsub(paste("[^", paste(alphabet, collapse = "", sep = ""), 
                     "]", sep = ""), alphabet[1], read)
  errorPos <- rep(1, length(qual)) < qual
  if (any(errorPos)) {
    for (i in which(errorPos)) {
      transProb <- prob[[substr(read, i, i)]]
      substr(read, i, i) <- sample(names(transProb), 1, 
                                   prob = transProb)
    }
  }
  read
}

pos2fastq1 <- function (readPos, names, quality, sequence, qualityFun, errorFun, 
                        readLen = 36, file, qualityType = c("Illumina", "Sanger", 
                                                            "Solexa"), ...) 
{
  if (file != "" && !is(file, "connection") && !file.exists(file)) 
    file <- file(file, open = "w", blocking = FALSE)
  replaceProb <- if (is.null(list(...)$prob)) 
    defaultErrorProb1()
  else match.fun(list(...)$prob)
  qualityFun <- match.fun(qualityFun)
  errorFun <- match.fun(errorFun)
  for (i in 1:2) {
    for (j in 1:length(readPos[[i]])) {
      readSeq <- ChIPsim::readSequence(readPos[[i]][j], sequence, 
                              strand = ifelse(i == 1, 1, -1), readLen = readLen)
      readQual <- qualityFun(readSeq, quality, ...)
      #readSeq <- errorFun(readSeq, decodeQuality(readQual, type = qualityType), prob = replaceProb)
      ChIPsim::writeFASTQ(as.character(readSeq), as.character(readQual), 
                 names[[i]][j], file = file, append = TRUE)
    }
  }
  invisible(sum(sapply(readPos, length)))
}


#generate read names
ReadNames <- paste("read_", 1:Nreads, sep="")

###################################################
### code chunk number 11: transitions
###################################################
transition <- list(Binding=c(Background=1), Background=c(Binding=BindingProb, Background=BackgroundProb))
transition <- lapply(transition, "class<-", "StateDistribution")

transition0 <- list(Binding=c(Background=1), Background=c(Binding=0, Background=1))
transition0 <- lapply(transition0, "class<-", "StateDistribution")


###################################################
### code chunk number 12: initial
###################################################
init <- c(Binding=0, Background=1)
class(init) <- "StateDistribution"


###################################################
### code chunk number 13: bgEmission
###################################################
backgroundFeature <- function(start, length=BackgroundFeatureLength, shape=shape1, scale=scale1){
  weight <- rgamma(1, shape=shape1, scale=scale1)
  params <- list(start = start, length = length, weight = weight)
  class(params) <- c("Background", "SimulatedFeature")
  
  params
}


###################################################
### code chunk number 14: bindingEmission
###################################################
bindingFeature <- function(start, length=BindingFeatureLength, shape=shape1, scale=scale1, enrichment=enrichment1, r=r1){
  stopifnot(r > 1)
  
  avgWeight <- shape * scale * enrichment
  lowerBound <- ((r - 1) * avgWeight)
  weight <- actuar::rpareto1(1, r, lowerBound)
  
  params <- list(start = start, length = length, weight = weight)
  class(params) <- c("Binding", "SimulatedFeature")
  
  params
}


###################################################
### code chunk number 15: features1_1
###################################################

generator <- list(Binding=bindingFeature, Background=backgroundFeature)

###################################################
### code chunk number 20: featureDensity1
###################################################
constRegion <- function(weight, length) rep(weight, length)
# featureDensity.Binding <- function(feature, ...) constRegion(feature$weight, feature$length)
featureDensity.Background <- function(feature, ...) constRegion(feature$weight, feature$length)




##################################################
## code chunk number 24: reconcileFeatures
##################################################
reconcileFeatures.TFExperiment <- function(features, ...){
  bindIdx <- sapply(features, inherits, "Binding")
  if(any(bindIdx))
    bindLength <- features[[min(which(bindIdx))]]$length
  else bindLength <- 1
  lapply(features, function(f){
    if(inherits(f, "Background"))
      f$weight <- f$weight/bindLength
    ## The next three lines (or something to this effect)
    ## are required by all 'reconcileFeatures' implementations. 
    f$overlap <- 0
    currentClass <- class(f)
    class(f) <- c(currentClass[-length(currentClass)], 
                  "ReconciledFeature", currentClass[length(currentClass)])
    f
  })
}



###################################################
### code chunk number 27: featureDensity2
###################################################
featureDensity.Binding <- function(feature, ...){
  featDens <- numeric(feature$length)
  featDens[floor(feature$length/2)] <- feature$weight
  featDens
}





###################################################
### code chunk number 29: fragmentLength
###################################################
fragLength <- function(x, minLength, maxLength, meanLength, ...){
  sd <- (maxLength - minLength)/4
  prob <- dnorm(minLength:maxLength, mean = meanLength, sd = sd)
  prob <- prob/sum(prob)
  prob[x - minLength + 1]
}





###################################################
### code chunk number 32: readLoc2
###################################################
set.seed(seed2)

GenerateChipSeqFastqFiles <- function(ExpNo) {
  #print("test 1")
  features <- ChIPsim::placeFeatures(generator, transition, init, start = 0, length = chrLen, globals=list(shape=shape1, scale=scale1),
                                     experimentType="TFExperiment", lastFeat=c(Binding = FALSE, Background = TRUE), 
                                     control=list(Binding=list(length=BindLength)))
  BindingVec <- vector(mode="character")
  StartVec <- vector(mode="numeric")
  LengthVec <- vector(mode="numeric")
  WeightVec <- vector(mode="numeric")
  
  for(i in 1:length(features)) {
    BindingVec[i] <- class(features[[i]])[1]
    StartVec[i] <- features[[i]]$start
    LengthVec[i] <- features[[i]]$length
    WeightVec[i] <- features[[i]]$weight
  }
  
  FeaturesResult <- data.frame(cbind(Bind=BindingVec, Start=StartVec, Length=LengthVec, Weight=WeightVec))
  write.table(FeaturesResult, paste(Feat_FileName, "_Chip_Seq_", ExpNo,".txt",sep=""), sep="\t", row.names=FALSE)
  #print("test 2")
  #create features for the input data
  features0 <- features
  bindIdx <- sapply(features, inherits, "Binding")
  BindIndices <- which(bindIdx)
  for(i in BindIndices) {
    class(features0[[i]]) <- class(features0[[i+1]])
    features0[[i]]$weight <- features0[[i+1]]$weight  
  }
  
  dens <- ChIPsim::feat2dens(features, length = chrLen)
  dens0 <- ChIPsim::feat2dens(features0, length = chrLen)
  
  #print("test 3")
  
  readDens <- ChIPsim::bindDens2readDens(dens, fragLength, bind = BindLength, minLength = MinLength, maxLength = MaxLength, meanLength = MeanLength) 
  readDens0 <- ChIPsim::bindDens2readDens(dens0, fragLength, bind = BindLength, minLength = MinLength, maxLength = MaxLength, meanLength = MeanLength) 
  
  #print("test 4")
  
  readLoc <- ChIPsim::sampleReads(readDens, Nreads)
  readLoc0 <- ChIPsim::sampleReads(readDens0, Nreads)
  
  #print("test 5")
  
  names <- list(paste("read", 1:length(readLoc[[1]]), sep="_"), paste("read", (1+length(readLoc[[1]])):(Nreads), sep="_"))
  names0 <- list(paste("read", 1:length(readLoc0[[1]]), sep="_"), paste("read", (1+length(readLoc0[[1]])):(Nreads), sep="_"))
  
  #print("test 6")
  
  pos2fastq1(readPos=readLoc, names = names,  sequence=chromosomes, qualityFun=randomQuality, errorFun=readError1, readLen = LengthReads, file=paste(Fast_FileName,"_Chip_Seq_", ExpNo,".fastq",sep=""), qualityType = c("Illumina"))
  pos2fastq1(readPos=readLoc0, names = names0,  sequence=chromosomes, qualityFun=randomQuality, errorFun=readError1, readLen = LengthReads, file=paste(Fast_FileName, "_Chip_Seq_Input_", ExpNo,".fastq",sep=""), qualityType = c("Illumina"))
  
  #print("test 7")
}
#lapply(5:6, GenerateChipSeqFastqFiles)
#output binding events
a <- proc.time()
sfClusterEval(ls())
sfExportAll()
sfClusterSetupRNG(type="RNGstream", seed = seed2)
sfClusterApplyLB(1:Nexp, GenerateChipSeqFastqFiles)
sfStop()
b <- proc.time()
print(b-a)

sfStop()
