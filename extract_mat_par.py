import sys


def main():

    counter = 0

    for line in sys.stdin:

        counter += 1
        line = line.rstrip().split()

        # print header only once
        if line[0].startswith('Off') and counter == 1:
            print('\t'.join(line))
            continue

        father, mother = line[1:3]

        if '*' in father and '#' in mother:
            continue

        else:
            print('\t'.join(line))


if __name__ == '__main__':
    main()
