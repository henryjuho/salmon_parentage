import argparse


def duplicates_to_rm(duplicates):

    """
    lists repeat indivs to remove
    :param duplicates: str
    :return: set
    """

    to_rm = set()

    for line in open(duplicates):

        line = line.rstrip().split(',')

        to_rm |= {line[0]}

    return to_rm


def get_gender(geno_file):

    """
    use original geno data to determine sex of individuals
    :param geno_file: str
    :return: dict
    """

    id_dict = {}

    sdy = 0

    for line in open(geno_file):

        line = line.rstrip().split(',')

        if line[0] == '':

            sdy = line.index('SDY_ion2')
            continue

        fish = line[0]
        if line[sdy] == '1':
            gender = 'male'
        elif line[sdy] == '0':
            gender = 'female'
        else:
            gender = 'unknown'

        id_dict[fish] = gender

    return id_dict


def estimate_birth_year(fish_id):

    """
    crudely estimates birth year from ID
    :param fish_id: str
    :return: str
    """

    fish_id = fish_id.upper()

    # get young
    if 'Y' in fish_id:
        age = fish_id.split('Y')[0].split('_')[-1]
        catch_year = 2000 + int(fish_id.split('_')[1])
        birth_year = catch_year - int(age)

    # rest should be adults
    elif '#' in fish_id or '*' in fish_id:
        birth_year = 'unknown'

    elif 'A' in fish_id:
        #  catch_year = 2000 + int(fish_id.split('A')[0].split('_')[1])
        #  birth_year = catch_year - 5
        birth_year = 'unknown'

    elif fish_id.startswith('UTS'):
        # catch_year = 2011
        # birth_year = catch_year - 5
        birth_year = 'unknown'

    else:
        birth_year = 'unknown'

    return str(birth_year)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-in_dat', help='colony sorted output', action='append', required=True)
    parser.add_argument('-geno', help='filtered genotype csv', required=True)
    parser.add_argument('-duplicates', help='list of duplicates from colony', required=True)
    args = parser.parse_args()

    # list of duplicate ids
    dups = duplicates_to_rm(args.duplicates)

    col_dat = []
    for y in args.in_dat:
        col_dat += open(y).readlines()

    gender_dict = get_gender(args.geno)

    # get unique parent ids
    parent_ids = [x.split()[1:3] for x in col_dat[1:]]
    unique_parents = []
    for pair in parent_ids:
        for indiv in pair:
            if indiv not in unique_parents:
                unique_parents.append(indiv)

    # set of offspring ids
    offspring_ids = set([x.split()[0] for x in col_dat[1:]])

    print('id', 'dam', 'sire', 'birth_year', 'gender', sep=',')

    # print offspring
    for line in col_dat[1:]:
        line = line.split()

        # check if dup
        if line[0] in dups:
            continue

        # get gender
        if line[0] in gender_dict.keys():
            gender = gender_dict[line[0]]
        else:
            gender = 'NA'

        # get birth year estimate
        birth_year = estimate_birth_year(line[0])

        out_line = line[:3] + [birth_year, gender]
        print(*out_line, sep=',')

    # print adults
    for fish in unique_parents:

        # check if dup
        if fish in dups:
            continue

        if fish in offspring_ids:
            continue

        # get gender
        if fish in gender_dict.keys():
            gender = gender_dict[fish]
        else:
            gender = 'unknown'

        # get birth year estimate
        birth_year = estimate_birth_year(fish)

        print(fish, 'NA', 'NA', birth_year, gender, sep=',')


if __name__ == '__main__':
    main()
