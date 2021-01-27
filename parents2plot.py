import sys


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

    dams = {}
    sires = {}

    for line in sys.stdin:

        if line.startswith('"id"'):
            continue

        else:

            line = line.replace('"', '').rstrip()

            offspring, dam, sire, LLRdam, LLRsire, LLRpair, OHdam, OHsire, MEpair = line.split(',')
            year, age = catch_age(offspring)

            # update dam dict
            if dam not in dams.keys():
                dams[dam] = {}

            if year not in dams[dam].keys():
                dams[dam][year] = {}

            if age not in dams[dam][year].keys():
                dams[dam][year][age] = 0

            dams[dam][year][age] += 1

            # update sire dict - lazy coding
            if sire not in sires.keys():
                sires[sire] = {}

            if year not in sires[sire].keys():
                sires[sire][year] = {}

            if age not in sires[sire][year].keys():
                sires[sire][year][age] = 0

            sires[sire][year][age] += 1

    # output plot csv
    print('id', 'offspring_year', 'offspring_age_class', 'parent_type', 'parent_year', 'parent_age_class', sep=',')
    # dams
    for d in dams.keys():
        d_year, d_age = catch_age(d)
        for y in dams[d].keys():
            for a in dams[d][y].keys():

                print(d, y, a, dams[d][y][a], 'dam', d_year, d_age, sep=',')

    # sires
    for s in sires.keys():
        s_year, s_age = catch_age(s)
        for y in sires[s].keys():
            for a in sires[s][y].keys():
                print(s, y, a, sires[s][y][a], 'sire', s_year, s_age, sep=',')


if __name__ == '__main__':
    main()
