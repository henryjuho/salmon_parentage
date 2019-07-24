#!/usr/bin/env python

import argparse
from create_dat_file import colony_header, colony_marker_info
from colony2ped import estimate_birth_year


def split_genos_by_birth_year(geno_file_name):

    genotype_data = open(geno_file_name).readlines()

    markers = genotype_data[0].rstrip().split(',')[1:]

    genos_by_year = {}

    for line in genotype_data[1:]:

        line = line.rstrip().split(',')
        fish_id = line[0]

        # skip adults
        if 'Y' not in fish_id.upper():
            continue

        # add birth year to dict if not there already
        birth_year = int(estimate_birth_year(fish_id))
        if birth_year not in genos_by_year.keys():
            genos_by_year[birth_year] = [markers]

        # add to relevant year
        genos_by_year[birth_year].append(line)

    return genos_by_year


def colony_geno_dat_all(genos, sex='both'):

    """
    gets geno information for candidates and offspring
    :param genos: list
    :param sex: str
    :return: dict
    """

    marker_list = genos[0]
    sdy = marker_list.index('SDY_ion2')
    out_marker_list = [x for x in marker_list if x != 'SDY_ion2']

    col_genos = []

    processed_fish = set()

    # process genotype data for offspring, male candidates, female candidates
    for line in genos[1:]:

        fish = line[0]

        # skip repeat individuals
        if fish in processed_fish:
            continue

        processed_fish |= {fish}

        alleles = line[1:]

        # assign sex
        if alleles[sdy] == '1':
            # gender = 'male'
            if sex == 'female':
                continue

        elif alleles[sdy] == '0':
            # gender = 'female'
            if sex == 'male':
                continue

        else:
            # gender = 'ambig'
            if sex != 'both':
                continue

        # remove sdy allele column
        del alleles[sdy]

        # recode genos
        allele_dict = {'1': '1 1', '2': '1 2', '3': '2 2', 'NA': '0 0'}
        alleles = [allele_dict[z] for z in alleles]
        recode_line = [line[0]] + alleles
        recode_line = ' '.join(recode_line)

        col_genos.append(recode_line)

    return out_marker_list, col_genos


def main():

    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-geno', help='CSV file containing genotypes', required=True)
    parser.add_argument('-marks', help='CSV file providing data on marker error', required=True)
    parser.add_argument('-run_length', choices=[1, 2, 3, 4], type=int, default=2)
    parser.add_argument('-precision', choices=[0, 1, 2, 3], type=int, default=1)
    args = parser.parse_args()

    # split geno data by year for young individuals only
    year_genos = split_genos_by_birth_year(args.geno)
    years = sorted(list(year_genos.keys()))

    # now loop and do a run for each year as adults and relevant offspring years?
    for year in years:

        run_name = 'uts_salmon_juv_{}'.format(year)
        dat_name = run_name + '.dat'

        off_spring_ys = list(range(year+2, years[-1]+1))

        # skip those that dont have off year data
        if len(off_spring_ys) == 0:
            continue

        cand_m = colony_geno_dat_all(year_genos[year], sex='male')
        cand_f = colony_geno_dat_all(year_genos[year], sex='female')

        marker_list = cand_m[0]

        # gather offspring
        off_spring_genos = [marker_list]  # start off with marker list
        for y in off_spring_ys:
            off_spring_genos += colony_geno_dat_all(year_genos[y])[1:]  # exclude marker lists

        # can then construct marker info
        marker_str = colony_marker_info(ordered_marker_list=marker_list, marker_file=args.marks)

        # get header info
        head = colony_header(dataset_name=run_name, n_snp=len(marker_list),
                             n_offspring=len(off_spring_genos[1][1:]),
                             run_l=args.run_length, prec=args.precision)

        with open(dat_name, 'w') as dat:
            print(head, file=dat)
            print(marker_str, file=dat)
            print('\n'.join(off_spring_genos[1][1:])+'\n', file=dat)

            # print info about parents
            print(0.10, 0.10, '! prob father and mother included in candidates', sep=' ', file=dat)
            print(len(cand_m[1][1:]), len(cand_f[1][1:]),
                  '   ! number of candidate males and females\n', sep=' ', file=dat)

            print('\n'.join(cand_m[1][1:])+'\n', file=dat)
            print('\n'.join(cand_f[1][1:])+'\n', file=dat)

            # print additional info fields that we lack data for
            print('0 0 ! Number of offspring with known paternity, exclusion threshold', file=dat)
            print('0 0 ! Number of offspring with known maternity, exclusion threshold', file=dat)
            print('0 ! Number of known paternal sibship', file=dat)
            print('0 ! Number of known maternal sibship', file=dat)
            print('0 ! Number of offspring with known excluded paternity', file=dat)
            print('0 !Number of offspring with known excluded maternity', file=dat)
            print('0 !Number of offspring with known excluded paternal sibships', file=dat)
            print('0 !Number of offspring with known excluded maternal sibships', file=dat)


if __name__ == '__main__':
    main()
