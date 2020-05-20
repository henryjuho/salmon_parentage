def extact_uts(csv):

    """
    gets uts trios from microsat ped
    :param csv: str
    :return: list
    """
    uts_sal = []

    for line in open(csv):

        # skip header
        if line.startswith('OffspID'):
            continue
        else:

            fish_trio = line.rstrip().split(',')[:3]  # off, dam, sire

            # get the teno samples
            if 'Uts' in fish_trio[0]:

                fish_trio_cleaned = []

                for fish in fish_trio:
                    if 'Uts' not in fish:
                        fish_trio_cleaned.append('NA')
                        continue

                    # reformat weirdly named 2015 samples
                    if '2015' in fish:

                        fish_parts = fish.split('_')
                        reconfig_fish = 'UTS_15_{}_{}'.format(fish_parts[1].lower(), fish_parts[3])
                        fish_trio_cleaned.append(reconfig_fish.upper())
                        continue

                    # make Uts UTS
                    fish_trio_cleaned.append(fish.replace('Uts', 'UTS').upper())

                uts_sal.append(fish_trio_cleaned)

    return uts_sal


def get_snp_ped_matches(snp_csv, micro_ids):

    """
    gets fish from snp ped that were also in microsat one
    :param snp_csv: str
    :param micro_ids: set
    :return: dict
    """

    snp_ped_dict = {}

    for line in open(snp_csv):

        # skip header
        if line.startswith('id'):
            continue

        off, dam, sire = line.rstrip().split(',')[:3]

        if off.upper() in micro_ids:
            if '*' in dam:
                dam = 'NA'
            if '#' in sire:
                sire = 'NA'

            snp_ped_dict[off.upper()] = [dam.upper(), sire.upper()]

        # skip offspring IDs that were not in microsat ped
        else:
            continue

    return snp_ped_dict


def main():

    with open('microsat_snp_parentage_comparison.csv', 'w') as raw_out:
        micro_ped = 'ParentageAssignments_microsat.csv'
        micro_sat_trios = extact_uts(micro_ped)
        off_ids = {x[0] for x in micro_sat_trios}

        # loop through microsat ids and extract corresponding ids from snp ped
        snp_ped = 'uts_ped.csv'
        matching_snp_ids = get_snp_ped_matches(snp_ped, off_ids)

        print('offspring', 'microsat_dam', 'microsat_sire', 'snp_dam', 'snp_sire', sep=',', file=raw_out)

        n_micro_off = 0
        n_miss_snp = 0
        n_in_both = 0
        n_parents_agree = 0
        n_par_only_in_micro = 0
        n_par_only_in_snp = 0
        snp_unassigned = 0
        micro_unassigned = 0

        for trio in micro_sat_trios:

            n_micro_off += 1

            try:
                snp_dat = matching_snp_ids[trio[0]]
                n_in_both += 1

            except KeyError:
                n_miss_snp += 1
                snp_dat = ['id_miss', 'id_miss']

            out_dat = trio + snp_dat
            print(*out_dat, sep=',', file=raw_out)

            # check parent agreement
            micro_dat = trio[1:]
            snp_unassigned += snp_dat.count('NA')
            micro_unassigned += micro_dat.count('NA')

            micro_pars = [x for x in micro_dat if x != 'NA']
            snp_pars = [x for x in snp_dat if x != 'NA' and x != 'id_miss']

            if len(micro_pars + snp_pars) == 0:
                continue

            # parents agree
            if sorted(micro_pars) == sorted(snp_pars):
                if len(micro_pars) == 1:
                    n_parents_agree += 1
                elif len(micro_pars) == 2:
                    n_parents_agree += 2

            else:

                # unique parents
                for y in micro_pars:
                    if y not in snp_pars:
                        n_par_only_in_micro += 1
                    else:
                        n_parents_agree += 1

                for y in snp_pars:
                    if y not in micro_pars:
                        n_par_only_in_snp += 1

    # summary output
    n_micro_pars = (n_micro_off * 2) - micro_unassigned
    n_snp_pars = (n_in_both * 2) - snp_unassigned

    summary = ('|Category | Count | Proportion |\n'
               '|:--------|:-----:|:-------:|\n'
               '| uts offspring in microsats | ' + str(n_micro_off) + ' | 1.000 |\n'
               '| uts offspring also in snp  | ' + str(n_in_both) + ' | ' + str(round(n_in_both/n_micro_off, 3)) + ' |\n'
               '| microsat parents assigned  | ' + str(n_micro_pars) + ' |' + str(round(n_micro_pars/(2*n_micro_off), 3)) + '|\n'
               '| snp parents assigned       | ' + str(n_snp_pars) + ' | ' + str(round(n_snp_pars/(2*n_in_both), 3)) + '|\n'
               '| parent agreement        | ' + str(n_parents_agree) + '|' + str(round(n_parents_agree/n_snp_pars, 3)) + '|\n')

    print(summary)


if __name__ == '__main__':
    main()
