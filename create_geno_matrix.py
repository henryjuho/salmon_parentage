#!/usr/bin/env python

import argparse


def read_geno_file(geno_file_name):

    """
    reads in file to allow loop across columns
    :param geno_file_name: str
    :return: list
    """

    geno_data = []

    for line in open(geno_file_name):

        line = line.rstrip().replace('"', '').split('\t')

        # adds column name for ids and populates list entry
        if line[0].startswith('AK'):
            line = ['ID'] + line
            geno_data = [[x] for x in line]
            continue

        # then populates each column
        for i in range(0, len(geno_data)):
            geno_data[i].append(line[i])

    return geno_data


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


def pass_maf_filter(genos, maf=0.3):

    """
    filters values below specified maf
    :param genos: list
    :param maf: float
    :return: bool
    """

    freqs = {}

    # loop through all genotypes and count alleles
    for x in genos:

        # skip NA
        if x == 'NA':
            continue

        for allele in x:
            if allele not in freqs.keys():
                freqs[allele] = 0

            freqs[allele] += 1

    # catch all NA columns
    if len(freqs.items()) == 0:
        return False

    # calculate frequencies
    freq = list(freqs.values())[0] / sum(freqs.values())

    if freq > 0.5:
        freq = 1 - freq

    # filter
    return freq > maf


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

        # counts number of times reference allele is present
        code = geno.count(ref)

        return code


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-maf', default=0.3, type=float, required=False)
    args = parser.parse_args()

    geno_data = 'sal_parentage/SNPgeno_janlaine_020818.txt'

    genos = read_geno_file(geno_data)

    recoded = []

    for col in genos:

        # process id column
        if col[0] == 'ID':
            recoded.append(col)
            continue

        # sorts out genotypes
        snp_id = col[0]
        alleles = col[1:]

        # skips cols that are all NAs
        if len(set(alleles)) == 1 and alleles[0] == 'NA':
            continue

        # filter on maf
        if not pass_maf_filter(alleles, maf=args.maf):
            continue

        ref_proxy = pick_ref(alleles)

        geno_codes = [assign_geno_code(ref_proxy, x) for x in alleles]

        outline = [snp_id] + geno_codes

        recoded.append(outline)

    # swap back from columns to rows and output
    for i in range(0, len(recoded[0])):

        new_line = [recoded[n][i] for n in range(0, len(recoded))]

        print(*new_line, sep=',')


if __name__ == '__main__':
    main()
