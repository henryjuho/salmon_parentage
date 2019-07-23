import sys
import argparse


def fish_cat(fish_id, gender):

    fish_id = fish_id.upper()

    # catch ambig gender
    if gender == 'unknown':
        if 'GP' in fish_id:
            return 'g'
        elif 'Y' in fish_id:
            return 'u_off'
        else:
            return 'u_p'

    # get young
    if 'Y' in fish_id:
        return gender[0] + '_off'

    # rest should be adults
    else:
        return gender[0] + '_p'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f_off', help='recode female offspring', default='actual')
    parser.add_argument('-m_off', help='recode male offspring', default='actual')
    parser.add_argument('-u_off', help='recode unknown offspring', default='actual')
    parser.add_argument('-f_p', help='recode female parents', default='actual')
    parser.add_argument('-m_p', help='recode male parents', default='actual')
    parser.add_argument('-u_p', help='recode unknown parents', default='actual')
    parser.add_argument('-g', help='recode grand parents', default='actual')
    args = parser.parse_args()

    recode_dict = {'f_off': args.f_off, 'm_off': args.m_off, 'u_off': args.u_off,
                   'f_p': args.f_p, 'm_p': args.m_p, 'u_p': args.u_p, 'g': args.g}

    for line in sys.stdin:

        line = line.rstrip()

        if line.startswith('id'):
            print(line)
            continue

        line = line.split(',')

        ped_cat = fish_cat(fish_id=line[0], gender=line[4])

        if ped_cat is None:
            print(*line, sep=',')
            continue

        action = recode_dict[ped_cat]

        if action == 'actual':
            print(*line, sep=',')
            continue

        elif action == 'rm':
            continue

        else:
            line[3] = action
            print(*line, sep=',')


if __name__ == '__main__':
    main()
