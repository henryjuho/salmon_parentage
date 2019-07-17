#!/bin/bash

source ~/.bash_profile

#$-l h_rt=8:00:00
#$-l mem=6G
#$-l rmem=6G

#$-pe openmp 28
#$-P evolgen
#$-q evolgen.q

#$-N uts_sal_colony_job.sh
#$-o ./uts_sal_colony.out
#$-e ./uts_sal_colony.error

#$-V

cd /fastdata/bop15hjb/sal_colony
mpirun -np 28 ~/colony2/colony2p.ifort.impi2015.out IFN:/home/bop15hjb/salmon_parentage/uts_salmon_mediumrun.dat &> uts_sal_colony.log.txt
