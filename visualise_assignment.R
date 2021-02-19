library(ggplot2)
library(dplyr)
library(tidyr)
library(viridis)
library(optparse)


rm(list=ls())

setwd('~/salmon_parentage')

#=======================================================================================================================
#     set up commandline options
#=======================================================================================================================

option_list <- list(make_option("--parents", type="character",
                                help="Sequoia parents assignment", metavar="character"),
                    make_option("--out", type="character", default='debug',
                                help="output pdf name", metavar="character"))

opt_parser <- OptionParser(option_list=option_list)
opt <- parse_args(opt_parser)

#=======================================================================================================================
# Read in sequoia plot data and plot by parent and year (1 per page of pdf)
#=======================================================================================================================

sequoia_data <- read.csv(opt$parents)
sequoia_data$parent_year <- as.factor(sequoia_data$parent_year)

pdf(opt$out, paper='a4', width=8, height=11)

for (d in c('dam', 'sire')){
  for (y in levels(sequoia_data$parent_year)){

    plot_dat <- subset(sequoia_data, parent_year==y & parent_type==d)

    parent_plot <- ggplot(plot_dat, aes(x=offspring_year, y=id, colour=offspring_age_class, size=n_offspring)) +
      geom_point() +
      scale_colour_manual(values=viridis(7)) +
      ggtitle(paste(d, y, sep='s, ')) +
      theme(legend.position = 'bottom',
            plot.margin = margin(t=0, r=5.5, b=-5.5, l=5.5, unit = "pt"))

    print(parent_plot)

  }
}

dev.off()