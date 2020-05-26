#!/usr/bin/env python

import argparse
import random


def colony_header(dataset_name, n_snp, n_offspring, run_l, prec):

    """
    formats header section of colony dat file
    :param dataset_name: str
    :param n_snp: int
    :param n_offspring: int
    :param run_l: int
    :param prec: int
    :return: str
    """

    seed = random.randint(1, 100000)

    struct = ("{name}  ! Dataset name\n"
              "{name}  ! Output file name\n"
              "{n_off}        ! Number of offspring in the sample\n"
              "{n_snp}         ! Number of loci\n"
              "{seed}       ! Seed for random number generator\n"
              "0           ! 0/1=Not updating/updating allele frequency\n"
              "2           ! 2/1=Dioecious/Monoecious species\n"
              "0           ! 0/1=No inbreeding/inbreeding\n"
              "0           ! 0/1=Diploid species/HaploDiploid species\n"
              "0  0        ! 0/1=Polygamy/Monogamy for males & females\n"
              "1           ! 0/1=Clone inference =No/Yes\n"
              "0           ! 0/1=Full sibship size scaling =No/Yes\n"
              "0           ! 0,1,2,3=No,weak,medium,strong sibship size prior; mean paternal & meternal sibship\n"
              "0           ! 0/1=Unknown/Known population allele frequency\n"
              "1           ! Number of runs\n"
              "{run_l}           ! Length of run, short, medium, long, very long run\n"
              "0           ! monitor method\n"
              "10000       ! monitor interval\n"
              "0           ! GUI mode\n"
              "1           ! analysis method 0,1,2 pairwise like, full like, combo\n"
              "{precision}           ! precision 0,1,2,3 low,medium,high,vhigh\n"
              "").format(name=dataset_name, n_off=n_offspring, n_snp=n_snp, seed=seed,
                         run_l=run_l, precision=prec)

    return struct


def colony_marker_info(ordered_marker_list, marker_file):

    """
    formats marker section of dat file
    :param ordered_marker_list: list
    :param marker_file: str
    :return: str
    """

    markers_data = {x.split(',')[0]: x.rstrip().split(',')[4] for x in open(marker_file) if not x.startswith('marker')}

    out_markers = []
    marker_type = []
    out_drop = []
    other_error = []

    for snp in ordered_marker_list:

        out_markers.append(snp)
        marker_type.append('0')
        out_drop.append(markers_data[snp])
        other_error.append('0')

    mark_dat = ("{markers} !ordered marker list\n"
                "{marker_types} !marker type, 1,0 dominant,codominant add @ to set all to same otherwise list\n"
                "{dropout} !allelic dropout per locus\n"
                "{typing_error} !other typing error at each locus\n"
                "").format(markers=' '.join(out_markers),
                           marker_types=' '.join(marker_type),
                           dropout=' '.join(other_error),
                           typing_error=' '.join(other_error))

    return mark_dat


def colony_geno_dat(geno_file_name):

    """
    gets geno information for candidates and offspring
    :param geno_file_name: str
    :return: dict
    """

    genos = open(geno_file_name).readlines()

    marker_list = genos[0].rstrip().split(',')[1:]
    sdy = marker_list.index('SDY_ion2')
    marker_list.remove('SDY_ion2')

    offspring = []
    female_candidates = []
    male_candidates = []

    processed_fish = set()

    # process genotype data for offspring, male candidates, female candidates
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

        # assign sex
        if alleles[sdy] == '1':
            gender = 'male'
        elif alleles[sdy] == '0':
            gender = 'female'
        else:
            gender = 'ambig'

        # remove sdy allele column
        del alleles[sdy]

        # recode genos
        allele_dict = {'1': '1 1', '2': '1 2', '3': '2 2', 'NA': '0 0'}
        alleles = [allele_dict[z] for z in alleles]
        recode_line = [line[0]] + alleles
        recode_line = ' '.join(recode_line)

        # offspring
        if 'y' in line[0]:
            offspring.append(recode_line)

        # parents
        else:
            if gender == 'male':
                male_candidates.append(recode_line)

            elif gender == 'female':
                female_candidates.append(recode_line)
            else:
                continue

    # return data as a dict
    geno_dict = {'markers': marker_list, 'off': offspring, 'm_cand': male_candidates, 'f_cand': female_candidates}
    return geno_dict


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
    head = colony_header(dataset_name='uts_salmon', n_snp=len(geno_dat['markers']), n_offspring=len(geno_dat['off']),
                         run_l=args.run_length, prec=args.precision)

    print(head)
    print(marker_str)
    print('\n'.join(geno_dat['off'])+'\n')

    # print infor about parents
    print(0.10, 0.10, '! prob father and mother included in candidates', sep=' ')
    print(len(geno_dat['m_cand']), len(geno_dat['f_cand']), '   ! number of candidate males and females\n', sep=' ')

    print('\n'.join(geno_dat['m_cand'])+'\n')
    print('\n'.join(geno_dat['f_cand'])+'\n')

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
