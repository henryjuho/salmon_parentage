#!/usr/bin/env python


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
