#!/usr/bin/env python

import csv
import argparse
import datetime


def adult_age(age_file):

    adult_ages = {}
    with open(age_file, encoding="latin-1") as age_csv:
        for line in csv.reader(age_csv, delimiter=","):
            if line[0] == '':
                continue

            smolt_age, sea_age = line[14:16]

            if smolt_age == 'NA' or sea_age == 'NA':
                continue

            age = int(smolt_age) + int(sea_age)
            fish_id = line[1].replace('"', '')

            adult_ages[fish_id] = age

    return adult_ages


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-filtered_csv', help='Filtered csv file from snp_data_prep.py', required=True)
    parser.add_argument('-adult_csv', help='CSV with adult age estimates', required=True)
    args = parser.parse_args()

    date = str(datetime.date.today())

    id_info = args.filtered_csv
    adult_ages = args.adult_csv

    # adult_dict = adult_age(adult_ages)
    year_dict = {x.split(',')[1].replace('"', ''): x.split(',')[15]
                 for x in open(adult_ages) if not x.startswith('""')}

    # reformat id file

    # sex_codes: 1 = female,  2 = male,  3=unknown,  4=hermaphrodites,  all other numbers,letters, or NA
    sexes = {'M': 2, 'F': 1, 'NA': 'NA'}

    with open(date + '.uts_lifehist.csv', 'w') as lifehist:

        print('ID', 'Sex', 'BirthYear', sep=',', file=lifehist)
        for line in open(id_info):

            # skip header
            if line.startswith(','):
                continue

            # extract columns needed
            line = line.split(',')
            fish_id = line[0]
            sdy = line[4]

            # assign sex
            if sdy == '1':
                sex = 'M'
            elif sdy == '0':
                sex = 'F'
            else:
                sex = 'NA'

            sex = sexes[sex]

            # calculate birth year
            # catch_year = fish_id.split('_')[1]

            # if 'A' in catch_year:
            #     # age = 5 + int(age.replace('SW', ''))
            #     # birth_approx = (int(catch_year.replace('A', '')) + 2000) - 5
            #     try:
            #         birth_approx = (int(catch_year.replace('A', '')) + 2000) - adult_dict[fish_id]
            #     except KeyError:
            #         birth_approx = (int(catch_year.replace('A', '')) + 2000) - 6
            #
            # else:
            #     juv_age = int(fish_id.split('_')[2].replace('y', '').replace('pp', '').replace('-3', ''))
            #     birth_approx = int(catch_year) + 2000 - juv_age

            birth_approx = year_dict[fish_id]
            print(fish_id, sex, birth_approx, sep=',', file=lifehist)


if __name__ == '__main__':
    main()
