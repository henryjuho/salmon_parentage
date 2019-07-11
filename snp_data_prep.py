#!/usr/env/bin python

import re


def review_control(control_list, error_out):

    """
    takes the male control data and looks at geno call agreement per marker
    :param control_list: list
    :param error_out: str
    :return: None
    """

    with open(error_out, 'w') as error_file:

        control_dat = transpose_geno_data(control_list)

        print('marker', 'majority_call', 'different_call', 'NAs', 'error', sep=',', file=error_file)

        for marker in control_dat[1:]:

            marker_id = marker[0]
            genos = marker[1:]

            counts = sorted([[y, genos.count(y)] for y in set(genos)], key=lambda x: x[1], reverse=True)

            main_call = counts[0][1]
            other_counts = sum([y[1] for y in counts[1:] if y[0] != 'NA'])
            na_counts = sum([y[1] for y in counts[1:] if y[0] == 'NA'])
            error = other_counts / float(main_call + other_counts)

            print(marker_id, main_call, other_counts, na_counts, error, sep=',', file=error_file)


def transpose_geno_data(data_list):

    """
    reads in data list to allow loop across columns
    :param data_list: str
    :return: list
    """

    geno_data = []

    for line in data_list:

        # adds column name for ids and populates list entry
        if line[1].startswith('AK'):
            geno_data = [[x] for x in line]
            continue

        # then populates each column
        for i in range(0, len(geno_data)):
            geno_data[i].append(line[i])

    return geno_data


def main():

    # raw run data
    set_1 = open('sal_parentage/GenoScoreNUM_NextSeq-20190416.txt').readlines()
    set_3 = open('sal_parentage/GenoScoreNUM_Annukka_set3_NextSeq-20190619.txt').readlines()

    # check header order
    assert set_1[0] == set_3[0]

    sets = [(1, set_1), (3, set_3)]

    male_controls = []
    uts_samples = []
    low_call_ids = []

    # process all runs
    for run in sets:

        for line in run[1]:

            line = line.rstrip().split('\t')

            # skip header
            if line[0].startswith('AKAP11_4'):
                if run[0] == 1:
                    header = [''] + line
                    male_controls.append(header)
                    uts_samples.append(header)
                continue

            id_info = line[0]
            geno_calls = line[1:]

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
                    continue  # this should skip all non uts, non male control samples

            reformed_line = [fish_id] + geno_calls

            # filter samples with many NAs and output list of IDs, run and percent NAs
            percent_na = geno_calls.count('NA') / float(len(geno_calls))
            if percent_na > 0.8:
                fail_info = (fish_id, run[0], percent_na)
                low_call_ids.append(fail_info)
                continue

            # add ok UTS samples to list
            uts_samples.append(reformed_line)

    # summarise markers from controls
    review_control(male_controls, 'marker_summary.csv')

    # todo loci failing


if __name__ == '__main__':
    main()
