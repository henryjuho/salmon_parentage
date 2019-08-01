import itertools


def main():

    smaples_processed = 'all_samples_process.txt'
    failed = set([x.split(',')[0] for x in open('removed_indivs.csv') if not x.startswith('ID')])

    success_matrix = {}

    for fish in open(smaples_processed):

        fish = fish.rstrip()

        if fish == '':
            continue

        # get young
        if 'y' in fish:

            catch, age = fish.split('_')[1:3]

        # adults
        else:
            age = 'A'

            if '_' not in fish:
                catch = '11'
            else:
                catch = fish.split('_')[1].replace('A', '')

        # update matrix
        if catch not in success_matrix.keys():
            success_matrix[catch] = {}

        if age not in success_matrix[catch].keys():
            success_matrix[catch][age] = [0, 0]

        # add as processed
        success_matrix[catch][age][0] += 1

        # add as failed
        if fish in failed:
            success_matrix[catch][age][1] += 1

    print('catch_year', 'age', 'n', 'n_fail', 'percent_fail', sep=',')

    all_ages = [list(success_matrix[x].keys()) for x in success_matrix.keys()]
    all_ages = sorted(list(set(itertools.chain(*all_ages))))

    # out matrix
    for y in success_matrix.keys():
        for a in all_ages:

            try:
                n, n_fail = int(success_matrix[y][a][0]), int(success_matrix[y][a][1])
                p_fail = n_fail / n
                print(y, a, n, n_fail, p_fail, sep=',')
            except KeyError:
                print(y, a, 0, 0, 0, sep=',')


if __name__ == '__main__':
    main()
