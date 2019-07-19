#!/usr/bin/env python

import argparse
from create_dat_file import colony_header, colony_marker_info, colony_geno_dat


def main():

    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-geno', help='CSV file containing genotypes', required=True)
    parser.add_argument('-marks', help='CSV file providing data on marker error', required=True)
    parser.add_argument('-run_length', choices=[1, 2, 3, 4], type=int, default=2)
    parser.add_argument('-precision', choices=[0, 1, 2, 3], type=int, default=1)
    args = parser.parse_args()

    # first off get genotypes read in and sorted
    geno_dat = colony_geno_dat(args.geno)

    # can then construct marker info
    marker_str = colony_marker_info(ordered_marker_list=geno_dat['markers'], marker_file=args.marks)

    # get header info
    head = colony_header(dataset_name='uts_salmon_adults', n_snp=len(geno_dat['markers']),
                         n_offspring=len(geno_dat['m_cand']) + len(geno_dat['f_cand']),
                         run_l=args.run_length, prec=args.precision)

    print(head)
    print(marker_str)
    print('\n'.join(geno_dat['m_cand']))
    print('\n'.join(geno_dat['m_cand']) + '\n')

    # print info about parents
    print(0, 0, '! prob father and mother included in candidates', sep=' ')
    print(0, 0, '! number of candidate males and females', sep=' ')

    # print additional info fields that we lack data for
    print('0 0 ! Number of offspring with known paternity, exclusion threshold')
    print('0 0 ! Number of offspring with known maternity, exclusion threshold')
    print('0 ! Number of known paternal sibship')
    print('0 ! Number of known maternal sibship')
    print('0 ! Number of offspring with known excluded paternity')
    print('0 !Number of offspring with known excluded maternity')
    print('0 !Number of offspring with known excluded paternal sibships')
    print('0 !Number of offspring with known excluded maternal sibships')


if __name__ == '__main__':
    main()
