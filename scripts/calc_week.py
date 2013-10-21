import csv
import sys
from collections import defaultdict
from dateutil.parser import parse
from pprint import pprint

if len(sys.argv) != 2:
    print 'Missing week number argument'
    sys.exit(1)

cur_week = sys.argv[1]

likelihood = [[0 for x in xrange(12)] for x in xrange(12)]

with open('likelihood.csv') as handle:
    reader = csv.reader(handle)
    difficulty = 1
    for row in reader:
        catagory = 1
        for col in row:
            likelihood[difficulty][catagory] = int(col);
            catagory += 1
        difficulty += 1

champions = {}
with open('../data/all_weeks.csv') as handle:
    reader = csv.DictReader(handle, ['Week', 'Name', 'Difficulty', 'Since', 'Times'])

    for line in reader:
        if line['Week'] == cur_week:
            name = line['Name']
            difficulty = line['Difficulty']
            since = line['Since']

            champions[name] = {
                'name': name,
                'difficulty': difficulty,
                'since': since,
            }

for name in champions.keys():
    champ = champions[name]
    d = int(champ['difficulty'])
    catagory = int(champ['since'])
    if catagory >= 8 and catagory <= 10:
        catagory = 9
    elif catagory >= 11 and catagory <= 13:
        catagory = 10
    elif catagory > 13:
        catagory = 11
    champ['likelihood'] = likelihood[d][catagory]

for i in reversed(range(0,100)):
    for name in champions.keys():
        champ = champions[name]
        if champ['likelihood'] == i:
            print name + ' ' + str(i)
