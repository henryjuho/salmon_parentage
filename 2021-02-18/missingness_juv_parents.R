library(dplyr)
library(ggplot2)
library(stringr)
library(tidyr)

setwd('~/salmon_parentage/2021-02-18')

missing_dat <- read.delim('2021-02-18.all_samples_process.txt', header = F)
colnames(missing_dat) <- c('id', 'miss')

sires <- read.delim('2021-02-18.sires.txt')
sires$sex <- 'M'
colnames(sires) <- c('id', 'sex')

dams <- read.delim('2021-02-18.dams.txt')
dams$sex <- 'F'
colnames(dams) <- c('id', 'sex')

parents <- rbind(sires, dams)
parents$parent <- 'Y'

all_dat <- dplyr::full_join(missing_dat, parents)

all_dat$parent <- replace_na(all_dat$parent, 'N')

filtered_ids <- read.csv('2021-02-18.removed_indivs.csv')$ID

all_dat <- filter(all_dat, !id %in% filtered_ids)

all_dat$juv <- ifelse(str_detect(all_dat$id, 'A'), 'adult', 'juvenile')

png('missingness.png', width=9, height=9, units='in', res=320)

ggplot(all_dat, aes(x=parent, y=miss, fill=juv)) +
  geom_boxplot()

dev.off()