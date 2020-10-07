#!/usr/bin/env python

import argparse


def main():

    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-geno', help='CSV file containing genotypes', required=True)
    args = parser.parse_args()

    genos = open(args.geno).readlines()

    marker_list = genos[0].rstrip().split(',')[1:]
    sdy = marker_list.index('SDY_ion2')
    marker_list.remove('SDY_ion2')
    marker_list = [''] + marker_list
    print(*marker_list, sep=',')

    processed_fish = set()

    # process genotype data
    for line in genos[1:]:

        # catch empty lines from Kenyons original csv
        if ',,,,,,,,,,,,,,,,' in line:
            continue

        line = line.rstrip().split(',')
        fish = line[0]

        # skip repeat individuals
        if fish in processed_fish:
            continue

        processed_fish |= {fish}

        alleles = line[1:]

        # remove sdy allele column
        del alleles[sdy]

        # recode genos
        allele_dict = {'1': '0', '2': '1', '3': '2', 'NA': '-9'}
        alleles = [int(allele_dict[z]) for z in alleles]
        recode_line = [fish] + alleles

        print(*recode_line, sep=',')


if __name__ == '__main__':
    main()
