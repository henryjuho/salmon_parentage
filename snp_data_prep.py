#!/usr/env/bin python

import re
import sys
import datetime
import argparse


def clean_data(sample_dat, ld_markers, filtered_out, clean_out):

    """
    removes bad loci and specified loci
    :param sample_dat: list
    :param ld_markers: list
    :param filtered_out: str
    :param clean_out: str
    :return: None
    """

    samples = transpose_geno_data(sample_dat)
    clean = []

    with open(filtered_out, 'w') as removed_snps, open(clean_out, 'w') as clean_file:

        print('snp_id', 'proportion_missing', sep=',', file=removed_snps)

        for col in samples:

            # process id column
            if col[0] == '':
                clean.append(col)
                continue

            # sorts out genotypes
            snp_id = col[0]
            alleles = col[1:]

            # skips cols that are more than 40% NAs
            percent_na = alleles.count('NA') / float(len(alleles))
            if percent_na > 0.4:
                print(snp_id, percent_na, sep=',', file=removed_snps)
                continue

            # VIP = vgll3_Top, vgll3_mis1, vgll3, mis2, vgll3_topAlt, also SDY_ion2
            # filter specific loci here
            markers_toremove = [] + ld_markers

            if snp_id in markers_toremove:
                print(snp_id, percent_na, sep=',', file=removed_snps)
                continue

            # convert alleles to form for colony 1,3=homo, 2=hetero?
            # allele_dict = {'1': '11', '2': '12', '3': '22', 'NA': '00'}
            # alleles = [allele_dict[z] for z in alleles]

            # update clean data
            new_col = [snp_id] + alleles
            clean.append(new_col)

        # output clean data
        for i in range(0, len(clean[0])):

            reconstructed_line = [x[i] for x in clean]
            print(*reconstructed_line, sep=',', file=clean_file)


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

    parser = argparse.ArgumentParser()
    parser.add_argument('-in_file', help='input file', required=True)
    parser.add_argument('-miss', default=0.2, type=float)
    args = parser.parse_args()

    # data from Kenyon
    km_data = open(args.in_file)
    linked_markers = [x.rstrip() for x in open('linked_markers_toremove.txt')]

    male_controls = []
    uts_samples = []
    low_call_ids = []

    date = str(datetime.date.today())

    samples_processed = open(date + '.all_samples_process.txt', 'w')

    # process all runs

    for line in km_data:

        line = line.rstrip().split(',')

        # skip header
        if line[0].startswith('run'):

            header = [''] + line[7:]
            male_controls.append(header)
            uts_samples.append(header)
            continue

        sample_info = line[0:7]
        run_name, run, life_stage, year, id_info, class_var, notes = sample_info
        id_info = id_info.replace('O', '0')

        geno_calls = line[7:]

        # catch water controls
        if re.search(r'(?i)water', id_info):
            continue

        # extract male controls
        if 'Male' in id_info:
            male_controls.append(line)
            continue

        # extract uts ids - have uts1 - uts54 - 2011 adults
        # id_str = re.compile(r'(?i)(UTS_\d{2}A?_\d{,3}y?_?\d{,4})')
        # id_strb = re.compile(r'(?i)(UTS\d{2})')

        # try:
        #     fish_id = re.search(id_str, id_info).group().rstrip('_')
        #
        # except AttributeError:
        #
        #     try:  # this is for 2011 weirdly named samples
        #         fish_id = re.search(id_strb, id_info).group().rstrip('_')
        #
        #     except AttributeError:
        #         continue  # this should skip all non uts, non male control samples
        fish_id = id_info

        reformed_line = [fish_id] + geno_calls

        # filter samples with many NAs and output list of IDs, run and percent NAs
        percent_na = geno_calls.count('NA') / float(len(geno_calls))
        print(fish_id, percent_na, sep='\t', file=samples_processed)

        if percent_na > args.miss:
            fail_info = (fish_id, run, percent_na)
            low_call_ids.append(fail_info)
            continue

        # add ok UTS samples to list
        uts_samples.append(reformed_line)

    samples_processed.close()

    # output indiv removed
    with open(date + '.removed_indivs.csv', 'w') as rm_ids:

        print('ID', 'run', 'proportion_NA', sep=',', file=rm_ids)
        for indiv in low_call_ids:
            print(*indiv, sep=',', file=rm_ids)

    # summarise markers from controls
    # review_control(male_controls, 'marker_summary.csv')

    # now clean up data - remove low success loci and linked loci
    clean_data(uts_samples, ld_markers=linked_markers,
               filtered_out=date + '.removed_loci.csv', clean_out=date + '.uts_sal_allruns.filtered.csv')


if __name__ == '__main__':
    main()
