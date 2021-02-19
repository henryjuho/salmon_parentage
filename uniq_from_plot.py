f1 = '2021-01-28_uts_parentage.parents.plotable.csv'
f2 = '2021-01-26_uts_parentage.parents.plotable.csv'

parents_1 = set([x.split(',')[0] for x in open(f1).readlines()[1:]])
parents_2 = set([x.split(',')[0] for x in open(f2).readlines()[1:]])

parent_dif = parents_2 - parents_1

for line in open(f2):

    line = line.rstrip()

    if line.startswith('id'):
        print(line)

    if line.split(',')[0] in parent_dif:
        print(line)
