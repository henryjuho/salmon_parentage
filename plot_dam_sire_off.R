library(reshape2)
library(ggplot2)
library(plyr)
library(viridis)
library(dplyr)

generateXcoord <- function(size){

  if(size %% 2 != 0 & size != 1){   # Check if size is odd
    newsize <- size - 1
    interval <- 1/newsize
    x <- seq(0, 1, interval)
    }

  if(size %% 2 == 0){    # Check if size is even
    interval <- 1/size
    x <- seq(0, 1, interval)[-size-1] + diff(seq(0, 1, interval))/2
    }

  if(size == 1) x <- 0.5

  x
  }


ped_data = read.csv('uts_ped.csv', stringsAsFactors=F)

#ped_data = subset(ped_data, gender!='unknown')

# suse code
ped2 <- melt(ped_data, id.vars=c("id"), measure.vars=c("dam", "sire"))
ped2 <- ped2[-which(is.na(ped2$value)),]

names(ped2)[which(names(ped2) == "value")] <- "parent_id"
ped2$Group <- 1:nrow(ped2)

ped3 <- melt(ped2, id.vars = "Group", measure.vars=c("id", "parent_id"))

names(ped3)[3] <- "id"
ped3 <- join(ped3, ped_data[,c("id", "birth_year", "gender")])
ped3 = subset(ped3, gender!='unknown')

head(ped3)
str(ped3)
#~~ Create an object to save the x coordinates within
xcoords <- NULL
z = -1

for(i in sort(unique(ped3$birth_year))){

  # Extract the number of Unique IDs per year and generate X coords
  ids  <- unique(ped3$id[which(ped3$birth_year == i)])

  newx <- generateXcoord(length(ids)) # generate X coordinates

  # Append to xcoords
  new_dat = data.frame(id = ids)
  new_dat = dplyr::left_join(new_dat, subset(ped_data, select=c('id', 'dam', 'sire', 'gender')))
  if(z==-1 | z==5){
    new_dat = arrange(new_dat, gender, id)
    new_dat$x = newx * 5
  }else{
    new_dat = arrange(new_dat, dam, sire)
    new_dat$x = newx + z
  }
  z = z + 1
  xcoords <- rbind(xcoords, new_dat)

  rm(ids, newx)
  }

# Merge with ped3
ped3 <- join(ped3, xcoords)


# plot
png('sal_dam_sires.png', width=20, height=6, units='in', res=320)

birthyears <- sort(unique(ped3$birth_year))

ggplot(ped3, aes(x, -birth_year, colour=gender)) +
  geom_line(aes(group = Group), alpha = 0.1, colour='darkgrey') +
  geom_point() +
  theme_bw() +
  theme(legend.position=c(0.05, 0.35),
        legend.title     = element_blank(),
        axis.text.x      = element_blank(),
        axis.text.y      = element_text(colour = "darkgrey"),
        axis.ticks.y     = element_blank(),
        axis.ticks.x     = element_blank()) +
  theme(plot.margin = unit(c(1.5, 1.5, 1.5, 1.5), units = "cm")) +
  scale_y_continuous(breaks = -seq(min(birthyears), max(birthyears), 1),
                     labels =  seq(min(birthyears), max(birthyears), 1)) +
  scale_colour_manual(values=viridis(4)[1:3]) +
  labs(x = "", y = "")

dev.off()