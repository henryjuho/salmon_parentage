#! /usr/bin/env Rscript

library(sequoia)
library(reshape2)
library(ggplot2)
library(viridis)

setwd('/home/local/hbarton/salmon_parentage')

genos <- as.matrix(read.csv('sal_parentage/sal_geno_matrix_sequoia.csv', row.names=1))
life_hist = read.csv('sal_parentage/sal_lifehist_sequoia.csv')

# duplicate check & parentage assignment (takes few minutes)
# (maximum number of sibship-clustering iterations = 0)
# if genotyping error rate is unknown, start of high

ParOUT <- sequoia(GenoM = genos,  LifeHistData = life_hist, MaxSibIter = 0, Err=0.01, MaxMismatch=10)

# inspect duplicates (intentional or accidental)

#ParOUT$DupGenotype

# check if distr. of age-differences for each relative type is sensible

#PlotAgePrior(ParOUT$AgePriors)
long_age = melt(as.matrix(ParOUT$AgePriors))

pdf('sal_age_priors.pdf', width=6, height=4)

ggplot(long_age, aes(x=Var1, y=value, colour=Var2)) +
  geom_point(stat='identity') +
  geom_line(stat='identity') +
  scale_colour_viridis(discrete=T) + 
  labs(x='Age difference? should be 11year span?', y='AgePrior')

dev.off()

pdf('sequoia_qc.pdf', width=6, height=6)

stats <- SnpStats(genos, ParOUT$PedigreePar)

dev.off()

# polish dataset: remove one indiv. from each duplicate pair 
# (1st one, or one w lowest call rate) & drop high error rate SNPs
Geno2 <- genos[!rownames(genos) %in% ParOUT$DupGenotype$ID2, ]
#Geno2 <- Geno2[, which(stats[,"ER"]>50)]

#stats <- SnpStats(Geno2, ParOUT$PedigreePar)

SeqOUT <- sequoia(GenoM = Geno2, MaxSibIter = 20, Err=0.001)

#SummarySeq(SeqOUT)

# save results
save(SeqOUT, file="Sequoia_output_date.RData")
