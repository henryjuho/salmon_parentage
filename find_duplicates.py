import argparse


def is_duplicate(g1, g2, mismatch=0, exclude_nas=True):

    """
    compares two indivs and checks if clones
    :param g1: list
    :param g2: list
    :param mismatch: int
    :param exclude_nas: bool
    :return: bool
    """

    match = 0
    total = 0

    for i in range(0, len(g1)):

        # skip missing if specified
        if exclude_nas:
            if g1[i] == 'NA' or g2[i] == 'NA':
                continue

        # count matches
        if g1[i] == g2[i]:
            match += 1

        total += 1

    if total - match <= mismatch:
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-geno', help='genotypes', required=True)
    parser.add_argument('-mismatch', help='number of mismatches allowed', default=0, type=int)
    parser.add_argument('-include_na', help='if specified counts NA as genotype and a mismatch',
                        default=True, action='store_false')
    args = parser.parse_args()

    genos = open(args.geno).readlines()[1:]
    genos_b = genos

    # compare each individual
    for indiv in genos:

        id_1, genos_1 = indiv.split(',')[0], indiv.split(',')[1:]

        # against each other individual
        for comp_indiv in genos_b:

            id_2, genos_2 = comp_indiv.split(',')[0], comp_indiv.split(',')[1:]

            # avoid self self comparisons
            if id_1 == id_2:
                continue

            # compare genos
            if is_duplicate(genos_1, genos_2, mismatch=args.mismatch, exclude_nas=args.include_na):
                print(id_1, id_2, sep=',')

        # remove extra process indiv
        genos_b.remove(indiv)


if __name__ == '__main__':
    main()
