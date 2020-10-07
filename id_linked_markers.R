library(genetics)
library(dplyr)
library(tidyr)


recode_geno <- function (geno){

    if (is.na(geno)){return(NA)}
    else if(geno==3){return('A/A')}
    else if(geno==2){return('A/T')}
    else if(geno==1){return('T/T')}
    else{return(NA)}
}

args <- commandArgs(trailingOnly=TRUE)
genos <- read.csv(args[1])

#str(genos)
#levels(genos$class)
#levels(genos$type)

markers <- genos[,8:ncol(genos)]

#str(markers)

recoded_markers <- as.data.frame(apply(markers, c(1,2), recode_geno))
recoded_markers <- drop_na(recoded_markers)
#str(recoded_markers)

geno_coded <- as.data.frame(lapply(recoded_markers, genotype))
geno_coded <- makeGenotypes(geno_coded)

pairwise_ld <- LD(geno_coded)

#str(pairwise_ld)

# from Paul's script

#pairwise_ld$r[which(pairwise_ld$"r" > 0.5 & pairwise_ld$"r")]
#pairwise_ld$r[which(pairwise_ld$"P-value" < 0.05)]

#plot( pairwise_ld$r ~ pairwise_ld$"P-value" )
#plot( pairwise_ld$"D'" ~ pairwise_ld$"P-value" )

#LDtable(pairwise_ld$D) # this threw an error

#LDtable(pairwise_ld, which=c("D", "D'", "r", "X^2","P-value", "n"))
pairwise_ld.frame = data.frame(pairwise_ld$r)
#head(pairwise_ld.frame)

#dim(pairwise_ld.frame)
pairwise_ld.stacked.frame = data.frame(Locus = rownames(pairwise_ld.frame), stack(pairwise_ld.frame))
names(pairwise_ld.stacked.frame) = c("Locus1", "r", "Locus2")
pairwise_ld.stacked.frame = pairwise_ld.stacked.frame[,c(1,3,2)]
pairwise_ld.stacked.frame[which(pairwise_ld.stacked.frame$r>0.5),][order(pairwise_ld.stacked.frame[which(pairwise_ld.stacked.frame$r>0.5),]$Locus1),]
