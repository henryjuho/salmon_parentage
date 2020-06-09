#!/usr/bin/env python


def main():

    id_info = 'uts_sal_allruns.filtered.csv'

    # reformat id file

    # sex_codes: 1 = female,  2 = male,  3=unknown,  4=hermaphrodites,  all other numbers,letters, or NA
    sexes = {'M': 2, 'F': 1, 'NA': 'NA'}

    with open('uts_sal_allruns.filtered_lifehist.csv', 'w') as lifehist:

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
            catch_year = fish_id.split('_')[1]

            if 'A' in catch_year:
                # age = 5 + int(age.replace('SW', ''))
                birth_approx = (int(catch_year.replace('A', '')) + 2000) - 5
            else:
                birth_approx = int(catch_year) + 2000

            print(fish_id, sex, birth_approx, sep=',', file=lifehist)


if __name__ == '__main__':
    main()
