#!/usr/bin/env python

from qsub import q_sub
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-in_dat', help='location of .dat file', required=True)
    parser.add_argument('-np', help='number of cores', type=int, required=True)
    parser.add_argument('-out_dir', help='Output directory', required=True)
    args = parser.parse_args()

    out_pre = args.in_dat.split('/')[-1].replace('.dat', '')
    cmd = ['cd ' + args.out_dir]

    colony = ('mpirun -np {cores} ~/colony2/colony2p.ifort.impi2015.out '
              'IFN:{dat} &> {prefix}.log.txt'
              '').format(cores=args.np, dat=args.in_dat, prefix=out_pre)

    cmd.append(colony)

    q_sub(cmd, out=args.out_dir + out_pre, t=96, rmem=8, mem=6, tr=args.np, evolgen=True)


if __name__ == '__main__':
    main()
