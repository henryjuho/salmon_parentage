#!/usr/bin/env python


def pick_ref(genos):

    """
    takes list of genos and picks first non-NA haplotype as ref
    :param genos: list
    :return: str
    """

    if genos[0] != 'NA':
        ref_prox = genos[0][0]

    else:
        genos = genos[1:]
        ref_prox = pick_ref(genos)

    return ref_prox


def assign_geno_code(ref, geno):

    """
    assigns relevant sequoia code
    :param ref: str
    :param geno: str
    :return: int
    """

    if geno == 'NA':
        return -9

    else:

        base_dict = {'C': 'C', 'G': 'C', 'T': 'T', 'A': 'T'}

        ref = base_dict[ref]

        geno = ''.join([base_dict[x] for x in geno])

        # counts number of times reference allele is present
        code = geno.count(ref)

        return code


def main():

    geno_data = 'sal_parentage/SNPgeno_janlaine_020818.txt'

    for line in open(geno_data):

        line = line.rstrip().replace('"', '').split('\t')

        # catches header and ensures blank column name for ID column
        if not line[0].isnumeric():
            print('.,' + ','.join(line))
            continue

        # process data lines, uses first geno as reference
        fish_id = line[0]
        genos = line[1:]

        ref_proxy = pick_ref(genos)
        geno_codes = [assign_geno_code(ref_proxy, x) for x in genos]

        outline = [int(fish_id)] + geno_codes

        print(*outline, sep=',')


if __name__ == '__main__':
    main()
