#!/usr/bin/env python


def main():

    id_info = 'sal_parentage/SNPgeno_janlaine_IDs_020818_colfix.csv'
    genotype_data = 'SNPgeno_janlaine_020818.txt'

    # reformat id file

    # sex_codes: 1 = female,  2 = male,  3=unknown,  4=hermaphrodites,  all other numbers,letters, or NA
    sexes = {'M': 2, 'F': 1, 'NA': 'NA'}

    with open('sal_parentage/sal_lifehist_sequoia.csv', 'w') as lifehist:

        print('ID', 'Sex', 'BirthYear', sep=',', file=lifehist)
        for line in open(id_info):

            # skip header
            if line.startswith('ID'):
                continue

            # extract columns needed
            line = line.split(',')
            fish_id = line[0]
            sex = sexes[line[8]]

            # calculate birth year
            age = line[6]
            if 'SW' in age:
                age = 5 + int(age.replace('SW', ''))
            else:
                age = int(age)

            year = int(line[7])
            birth_year = year - age

            print(fish_id, sex, birth_year, sep=',', file=lifehist)


if __name__ == '__main__':
    main()
