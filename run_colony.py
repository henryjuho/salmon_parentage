#!/usr/bin/env python

from qsub import q_sub
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-in_dat', help='location of .dat file', required=True)
    parser.add_argument('-np', help='number of cores', type=int, required=True)
    args = parser.parse_args()

    cmd = ['cd /fastdata/bop15hjb/sal_colony']

    colony = ('mpirun -np {cores} ~/colony2/colony2p.ifort.impi2015.out '
              'IFN:{dat} &> uts_sal_colony.log.txt'
              '').format(cores=args.np, dat=args.in_dat)

    cmd.append(colony)

    q_sub(cmd, out='./uts_sal_colony', rmem=6, mem=6, tr=args.np, evolgen=True)


if __name__ == '__main__':
    main()
