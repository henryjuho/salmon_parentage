#!/usr/env/bin python

import re


def main():

    # raw run data
    set_1 = open('sal_parentage/GenoScoreNUM_NextSeq-20190416.txt').readlines()
    set_3 = open('sal_parentage/GenoScoreNUM_Annukka_set3_NextSeq-20190619.txt').readlines()

    assert set_1[0] == set_3[0]

    sets = [(1, set_1), (3, set_3)]

    male_controls = []

    uts_samples = []

    for run in sets:

        for line in run[1]:

            line = line.split('\t')

            # skip header
            if line[0].startswith('AKAP11_4'):
                if run[0] == 1:
                    header = [''] + line
                    male_controls.append(header)
                    uts_samples.append(header)
                continue

            id_info = line[0]

            # catch water controls
            if re.search(r'(?i)water', id_info):
                continue

            # extract male controls
            if 'Male' in id_info:
                male_controls.append(line)
                continue

            # extract uts ids - have uts1 - uts54 - 2011 adults
            id_str = re.compile(r'(?i)(UTS_\d{2}A?_\d{,3}y?_?\d{,4})')
            id_strb = re.compile(r'(?i)(UTS\d{2})')

            try:
                fish_id = re.search(id_str, id_info).group().rstrip('_')

            except AttributeError:

                try:  # this is for 2011 weirdly named samples
                    fish_id = re.search(id_strb, id_info).group().rstrip('_')

                except AttributeError:
                    continue

            reformed_line = [fish_id] + line[1:]

            # filter samples with many NAs and output list of IDs, run and percent NAs

            print(reformed_line)





    # todo indivs failing
    # todo loci failing
    # todo male controls for estimate of allele drop out


if __name__ == '__main__':
    main()
