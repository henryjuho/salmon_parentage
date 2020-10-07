def catch_age(id_str):

    if id_str == 'NA':

        return 'NA', 'NA'

    catch_year = id_str.split('_')[1]

    if 'A' in catch_year:
        age = 'A'
        catch_year = catch_year.replace('A', '')

    else:
        age = id_str.split('_')[2]

    return catch_year, age


def main():

    parents_file = 'uts_parents.csv'

    # data = {catch_year: {age: {mother: {catch_year: n}, father: {catch_year: n,}}}}
    sum_dat = {}

    for line in open(parents_file):

        line = line.rstrip().replace('"', '').split(',')
        if line[0] == 'id':
            continue

        indiv, dam, sire = line[0:3]

        # get current individual category
        catch, age_cat = catch_age(indiv)

        if catch not in sum_dat.keys():
            sum_dat[catch] = {}

        if age_cat not in sum_dat[catch].keys():
            sum_dat[catch][age_cat] = {'mother': {}, 'father': {}}

        # add dam info
        mother_catch = catch_age(dam)[0]

        if mother_catch not in sum_dat[catch][age_cat]['mother'].keys():
            sum_dat[catch][age_cat]['mother'][mother_catch] = 0

        sum_dat[catch][age_cat]['mother'][mother_catch] += 1

        # add sire info
        father_catch = catch_age(sire)[0]

        if father_catch not in sum_dat[catch][age_cat]['father'].keys():
            sum_dat[catch][age_cat]['father'][father_catch] = 0

        sum_dat[catch][age_cat]['father'][father_catch] += 1


    # output summary table
    all_years = ['NA'] + [str(x) for x in range(11, 20)]

    header = ['catch_year', 'age_cat'] + ['Dam_' + x for x in all_years] + ['Sire_' + x for x in all_years]

    print(*header, sep=',')

    for year in all_years:
        if year == 'NA':
            continue

        for age in sorted(sum_dat[year].keys()):

            mother_dat = []
            father_dat = []

            for y in all_years:

                try:
                    mother_dat.append(sum_dat[year][age]['mother'][y])
                except KeyError:
                    mother_dat.append(0)

                try:
                    father_dat.append(sum_dat[year][age]['father'][y])
                except KeyError:
                    father_dat.append(0)

            out_line = [year, age] + mother_dat + father_dat
            print(*out_line, sep=',')


if __name__ == '__main__':
    main()
