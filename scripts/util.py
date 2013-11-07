from collections import defaultdict
import csv, random
from dateutil.parser import parse
from pprint import pprint

METAS = ['top', 'mid', 'jungle', 'adc', 'support']

def categorize_since(input):
    """ Makes categories for weeks since a champion was free """
    if 0 <= input <= 7:
        return int(input)

    if 8 <= input <= 10:
        return 8

    if 11 <= input <= 13:
        return 9

    if input >= 14:
        return 10

def categorize_diff(input):
    """ Categorizes champion difficulties. """
    return int(input)

def compute_likelihoods(released):
    rv = {}

    for line in open('../data/free_champ_features.csv').readlines():
        parts = line.strip().split(',')

        week_num = int(parts[0])

        if week_num not in rv:
            rv[week_num] = {}

            if week_num > 0:
                rv[week_num][None] = rv[week_num - 1][meta].copy()
            else:
                rv[week_num][None] = defaultdict(int)

            for meta in METAS:
                if week_num > 0:
                    rv[week_num][meta] = rv[week_num - 1][meta].copy()
                else:
                    rv[week_num][meta] = defaultdict(int)

        difficulty = categorize_diff(parts[2])
        weeks_since_free = categorize_since(int(parts[3]))

        entry = (difficulty, weeks_since_free)
        times_free = parts[4]

        champ_meta = parts[5].split(':')
        for meta in champ_meta:
            #rv[week_num][meta][entry] += 1.0 / champion_count(released, week_num, meta)
            rv[week_num][meta][entry] += 1
        rv[week_num][None][entry] += 1.0
        #rv[week_num][None][entry] += 1.0 / champion_count(released, week_num)

    return rv

def print_matrix(matrix):
    rv = ""
    for i in range(1, 11):
        for j in range(0, 11):
            rv += "%d " % (matrix[(i,j)])

        rv += "\n"
    print rv

def champion_count(released, week_num, meta=None):
    count = 0
    for champ in released.keys():
        if not meta or meta in metas[champ]:
            if released[champ] <= week_num:
                count += 1
    return count


def compute_released_dates_difficulties():
    """ Computes the number of champions in each difficulty category """

    difficulties = {}
    for meta in METAS:
        difficulties[meta] = defaultdict(int)

    difficulties[None] = defaultdict(int)

    released = {}
    metas = defaultdict(list)
    with open('../data/champions.csv') as handle:

        reader = csv.DictReader(handle, ['Name', 'RP', 'IP', 'Popularity', 'Win Rate', 'Ban Rate', 'Meta', 'Released', 'Difficulty', 'RiotMeta'])

        i = 0
        for line in reader:
            if i == 0:
                i += 1
                continue
            name = line['Name']
            released_date = parse(line['Released'])

            champ_meta = line['RiotMeta'].split(':')

            release_week = (released_date - parse('2009-11-25')).days / 7

            if release_week < 0:
                release_week = 0
            released[name] = release_week

            for meta in champ_meta:
                difficulties[meta][categorize_diff(int(line['Difficulty']))] += 1

                metas[name].append(meta)

            difficulties[None][categorize_diff(int(line['Difficulty']))] += 1

    return released, difficulties, metas

def champion_features():
    """ Returns a list of all champions of the given meta and their features for the given week. """

    rv = {}
    with open('../data/all_weeks.csv') as handle:
        reader = csv.DictReader(handle, ['Week', 'Name', 'Difficulty', 'Since', 'Times', 'RiotMeta'])

        for line in reader:
            name = line['Name']
            difficulty = line['Difficulty']
            since = line['Since']
            times = int(line['Times'])

            champ_meta = line['RiotMeta'].split(':')

            week_num = int(line['Week'])

            if week_num not in rv:
                rv[week_num] = {}
                for meta in METAS:
                    rv[week_num][meta] = {}
                rv[week_num][None] = {}

            for meta in champ_meta:
                rv[week_num][meta][name] = {
                    'name': name,
                    'difficulty': difficulty,
                    'since': since,
                    'times': times,
                }

            #I shoud feel dirty for copy pasta.
            rv[week_num][None][name] = {
                'name': name,
                'difficulty': difficulty,
                'since': since,
                'times': times,
            }

        return rv

released, difficulties, metas = compute_released_dates_difficulties()
all_likelihoods = compute_likelihoods(released)
all_champions = champion_features()

def predict(curr_week, meta):
    curr_week = curr_week - 1

    #figure out when these doods were released.

    likelihoods = all_likelihoods[curr_week][meta]

    week_champions = all_champions[curr_week][meta]

    for name in week_champions.keys():
        champ = week_champions[name]
        d = categorize_diff(champ['difficulty'])
        category = categorize_since(int(champ['since']))

        times = champ['times']
        prior = float(times) / (int(curr_week) - released[name])

        num_difficulty = 1
        if d in difficulties[meta]:
            num_difficulty = difficulties[meta][d]

        avg = 0
        avg += likelihoods[(d, category)]

        champ['likelihood'] = avg / num_difficulty
        champ['prior'] = prior

    predictor = lambda x: -(x[1]['likelihood']*x[1]['prior'])
    predictions = sorted(week_champions.iteritems(), key=predictor)

    return predictions

def get_free_champs():
    """ Tells you who was actually free the given week """
    with open('../data/free_week.csv') as handle:
        rv = {}
        reader = csv.reader(handle, delimiter=',', quotechar='"')
        week_num = 0

        for line in reader:
            date = parse(line[0])
            free_champs = line[1:]

            rv[week_num] = free_champs

            week_num += 1
        return rv
