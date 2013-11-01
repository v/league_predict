import csv
import sys
from collections import defaultdict
from dateutil.parser import parse
from pprint import pprint

def categorize_since(input):
    if 0 <= input <= 7:
        return int(input)

    if 8 <= input <= 10:
        return 8

    if 11 <= input <= 13:
        return 9

    if input >= 14:
        return 10

def categorize_diff(input):
    return int(input)

def compute_likelihoods(curr_week, riotmeta):
    rv = defaultdict(int)
    for line in open('fuck').readlines():
        parts = line.strip().split(',')

        week_num = parts[0]

        if int(week_num) < int(curr_week):
            #difficulty = int(parts[2])
            difficulty = categorize_diff(parts[2])
            weeks_since_free = categorize_since(int(parts[3]))

            entry = (difficulty, weeks_since_free)
            times_free = parts[4]

            champ_meta = parts[5].split(':')
            if riotmeta in champ_meta:
                rv[entry] += 1

    return rv

def print_matrix(matrix):
    rv = ""
    for i in range(1, 11):
        for j in range(0, 11):
            rv += "%d " % (matrix[(i,j)])

        rv += "\n"
    print rv

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print 'Missing week number and meta argument'
        sys.exit(1)
    curr_week = str(int(sys.argv[1]) - 1)

    METAS = ['top', 'mid', 'jungle', 'adc', 'support']

    # the meta being checked
    check_meta = sys.argv[2]

    likelihoods = compute_likelihoods(curr_week, check_meta)

    #figure out when these doods were released.
    released = {}
    difficulties = defaultdict(int)
    with open('../data/champions.csv') as handle:

        reader = csv.DictReader(handle, ['Name', 'RP', 'IP', 'Popularity', 'Win Rate', 'Ban Rate', 'Meta', 'Released', 'Difficulty', 'RiotMeta'])

        i = 0
        for line in reader:
            if i == 0:
                i += 1
                continue
            name = line['Name']
            released_date = parse(line['Released'])

            riotmeta = line['RiotMeta'].split(':')

            release_week = (released_date - parse('2009-11-25')).days / 7

            if release_week < 0:
                release_week = 0
            released[name] = release_week

            if check_meta in riotmeta:
                difficulties[categorize_diff(int(line['Difficulty']))] += 1
    print difficulties

    champions = {}
    with open('../data/all_weeks.csv') as handle:
        reader = csv.DictReader(handle, ['Week', 'Name', 'Difficulty', 'Since', 'Times', 'RiotMeta'])

        for line in reader:
            if line['Week'] == curr_week:
                name = line['Name']
                difficulty = line['Difficulty']
                since = line['Since']
                times = int(line['Times'])

                riotmeta = line['RiotMeta'].split(':')

                if check_meta in riotmeta:
                    champions[name] = {
                        'name': name,
                        'difficulty': difficulty,
                        'since': since,
                        'times': times,
                    }

    for name in champions.keys():
        champ = champions[name]
        d = categorize_diff(champ['difficulty'])
        category = categorize_since(int(champ['since']))

        times = champ['times']
        prior = float(times) / (int(curr_week) - released[name])

        champ['likelihood'] = likelihoods[(d, category)] / difficulties[categorize_diff(champ['difficulty'])]
        champ['prior'] = prior

    sorted_list = sorted(champions.iteritems(), key=lambda x: -(x[1]['likelihood'] * x[1]['prior']) )

    for item in sorted_list:
        print item[0], item[1]
