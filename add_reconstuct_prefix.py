import sys


def main():

    for line in sys.stdin:

        line = line.replace('  #', sys.argv[1] + '#')
        line = line.replace('  *', sys.argv[1] + '*')

        print(line.rstrip())


if __name__ == '__main__':
    main()
