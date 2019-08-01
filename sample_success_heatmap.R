library(ggplot2)
library(viridis)

success = read.csv('sample_success_data.csv')

success$age = factor(success$age, levels=c('A', '0y', '1y', '2y', '3y'))
success$catch_year =factor(success$catch_year, levels=rev(c('11', '12', '13', '14', '15', '16', '17', '18')))

png('sample_heatmap.png', width=5, height=6, res=320, units='in')

ggplot(success, aes(x=age, y=catch_year)) +
    geom_tile(aes(fill=percent_fail)) +
    geom_text(aes(label = paste(n_fail, ' / ', n, sep='')), size = 3, colour='white') +
    scale_fill_viridis()

dev.off()