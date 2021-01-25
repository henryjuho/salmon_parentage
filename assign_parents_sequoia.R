library(sequoia)


# get in the right place
setwd('~/salmon_parentage')

# input
args <- commandArgs(trailingOnly=TRUE)
geno_file <- args[1]
#geno_file <- 'uts_sal_allruns.filtered.nosdy.recode.csv'
life_hist <- read.csv(args[2])
#life_hist <- read.csv('uts_sal_allruns.filtered_lifehist.csv')

out_stem <- paste('uts_parentage', Sys.Date(), sep='_')

#=======================================================================================================================
#     Initial run of sequia to ID duplicates and calc MAF
#=======================================================================================================================

genos <- as.matrix(read.csv(geno_file, row.names=1, stringsAsFactors=FALSE, strip.white = TRUE))
check_dat <- CheckGeno(genos)

assigned_parents <- sequoia(GenoM = genos, LifeHistData = life_hist, MaxSibIter = 0, MaxSibshipSize = 2000)

dups_csv <- paste(out_stem, 'duplicates.csv', sep='.')
to_remove <- paste(out_stem, 'duplicates.toremove.txt', sep='.')

write.csv(assigned_parents$DupGenotype, dups_csv, row.names=F)
system(paste('python dups_to_rm.py', dups_csv, sep=' '))

stats <- SnpStats(genos, assigned_parents$PedigreePar)
MAF <- ifelse(stats[,"AF"] <= 0.5, stats[,"AF"], 1-stats[,"AF"])

#=======================================================================================================================
#    Remove duplicates - retain Adult over juvenile and 0Y over older -filter on MAF
#=======================================================================================================================
to_remove <- read.delim(to_remove, header=F)

genos2 <- genos[!rownames(genos) %in% to_remove$V1, ]
genos2 <- genos2[, -which(MAF < 0.1)]

# Indiv.Mis <- apply(genos2, 1, function(x) sum(x == -9)) / ncol(genos2)
# genos2 <- genos2[Indiv.Mis < 0.2, ]

parents_final <- sequoia(GenoM = genos2, LifeHistData = life_hist, MaxSibIter = 0, Err = 0.0001, MaxSibshipSize = 2000)
seq_list <- list('Specs'=parents_final$Specs, 'AgePriors'=parents_final$AgePriors, 'ErrM'=parents_final$ErrM)

parents_2 <- sequoia(GenoM = genos2, LifeHistData = life_hist, Err = 0.0001, MaxSibshipSize = 2000, SeqList=list(AgePriors = parents_final$AgePriors), MaxSibIter=0)

out_csv <- paste(out_stem, 'parents.csv', sep='.')

write.csv(parents_2$PedigreePar, out_csv, row.names=F)
stats <- SnpStats(genos2, parents_2$PedigreePar)
