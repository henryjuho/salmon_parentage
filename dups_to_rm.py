import sys
import itertools


def main():

    matches = []

    for line in open(sys.argv[1]).readlines()[1:]:

        line = line.rstrip().replace('"', '').split(',')
        id1, id2 = line[2:4]

        if id1 not in itertools.chain(*matches) and id2 not in itertools.chain(*matches):
            matches.append({id1, id2})

        else:
            for group in matches:
                if id1 in group or id2 in group:
                    group |= {id1, id2}
                    break

    to_remove = []

    for match_set in matches:
        dups_by_year = sorted(list(match_set))

        adults = []
        for fish_id in dups_by_year:
            if 'A' in fish_id:
                adults.append(fish_id)

        if len(adults) == 0:
            keep = dups_by_year[0]
        else:
            keep = adults[0]

        dups_by_year.remove(keep)
        to_remove += dups_by_year

    out = sys.argv[1].replace('.csv', '.toremove.txt')

    with open(out, 'w') as outfile:
        print(*to_remove, sep='\n', file=outfile)


if __name__ == '__main__':
    main()
