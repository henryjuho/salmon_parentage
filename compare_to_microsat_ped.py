def extact_uts(csv):

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

    micro_ped = 'ParentageAssignments_microsat.csv'
    micro_sat_trios = extact_uts(micro_ped)
    off_ids = {x[0] for x in micro_sat_trios}

    # loop through microsat ids and extract corresponding ids from snp ped
    snp_ped = 'uts_ped.csv'
    matching_snp_ids = get_snp_ped_matches(snp_ped, off_ids)

    print('offspring', 'microsat_dam', 'microsat_sire', 'snp_dam', 'snp_sire')

    for trio in micro_sat_trios:

        try:
            snp_dat = matching_snp_ids[trio[0]]
        except KeyError:
            snp_dat = ['id_miss', 'id_miss']

        out_dat = trio + snp_dat
        print(*out_dat)


if __name__ == '__main__':
    main()
