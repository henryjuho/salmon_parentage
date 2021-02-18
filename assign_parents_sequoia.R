library(sequoia)
library(optparse)
library(reshape2)
library(ggplot2)
library(viridis)


#=======================================================================================================================
#     set up commandline options
#=======================================================================================================================

option_list <- list(make_option("--geno", type="character",
                                default='2021-02-18.uts_sal_allruns.filtered.nosdy_recode.csv',
                                help="Filtered genotype file", metavar="character"),
                    make_option("--hist", type="character", default='2021-02-18.uts_lifehist.csv',
                                help="Life history data", metavar="character"),
                    make_option("--prior_type", type="numeric", default=0,
                                help="Prior adjustment, 0=default, 1=age gap of 3 for females and 1 for males and below
                                      set to zero, 2=priors < 0.1 set to zero", metavar="numeric"),
                    make_option("--out_tag", type="character", default='debug',
                                help="tag for output file name", metavar="character"))


opt_parser <- OptionParser(option_list=option_list)
opt <- parse_args(opt_parser)

# get in the right place
setwd('~/salmon_parentage')

geno_file <- opt$geno
life_hist <- read.csv(opt$hist)

out_stem <- paste(Sys.Date(), opt$out_tag, sep='.')
out_stem <- paste(out_stem, '.prior', as.character(opt$prior_type), sep='')

#=======================================================================================================================
#     Initial run of sequia to ID duplicates and calc MAF
#=======================================================================================================================

genos <- as.matrix(read.csv(geno_file, row.names=1, stringsAsFactors=FALSE, strip.white = TRUE))
check_dat <- CheckGeno(genos)

assigned_parents <- sequoia(GenoM = genos, LifeHistData = life_hist, MaxSibIter = 0, MaxSibshipSize = 2000)

dups_csv <- paste(out_stem, 'duplicates.csv', sep='.')
to_remove <- paste(out_stem, 'duplicates.toremove.txt', sep='.')

write.csv(assigned_parents$DupGenotype, dups_csv, row.names=F)
system(paste('python3 dups_to_rm.py', dups_csv, sep=' '))

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

#=======================================================================================================================
#    Run sequoia for initial parentage assignment to get age priors out
#=======================================================================================================================

parents_final <- sequoia(GenoM = genos2, LifeHistData = life_hist, MaxSibIter = 0, Err = 0.0001, MaxSibshipSize = 2000)

#=======================================================================================================================
#    Adjust age priors as specified
#=======================================================================================================================

age_ps <- parents_final$AgePriors

if (opt$prior_type == 1){
  # reset manual for Kenyon (row 1 - zero age gap already 0)
  # male 1 year age gap to zero
  age_ps[2, 2] <- 0

  # female age gaps up to 3 year age gap to zero
  age_ps[2, 1] <- 0
  age_ps[3, 1] <- 0
  age_ps[4, 1] <- 0
}

if (opt$prior_type == 2){
  # reset most unprobable age rels to 0 p
  age_ps[age_ps<0.1] <- 0
}

#=======================================================================================================================
#    Run sequoia again with previously output age priors as input
#=======================================================================================================================
pdf(paste(out_stem, 'plots.pdf', sep='.'), paper='a4')

sequoia::PlotAgePrior(age_ps)

parents_2 <- sequoia(GenoM = genos2, LifeHistData = life_hist, Err = 0.0001, MaxSibshipSize = 2000, SeqList=list(AgePriors = age_ps), MaxSibIter=0, UseAge='extra')

out_csv <- paste(out_stem, 'parents.csv', sep='.')

write.csv(parents_2$PedigreePar, out_csv, row.names=F)
stats <- SnpStats(genos2, parents_2$PedigreePar)

dev.off()