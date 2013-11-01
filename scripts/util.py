from collections import defaultdict
import csv, random
from dateutil.parser import parse

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

def compute_likelihoods(curr_week, riotmeta):
    rv = defaultdict(int)
    for line in open('fuck').readlines():
        parts = line.strip().split(',')

        week_num = int(parts[0])

        if week_num < curr_week:
            #difficulty = int(parts[2])
            difficulty = categorize_diff(parts[2])
            weeks_since_free = categorize_since(int(parts[3]))

            entry = (difficulty, weeks_since_free)
            times_free = parts[4]

            champ_meta = parts[5].split(':')
            if not riotmeta or riotmeta in champ_meta:
                rv[entry] += 1

    return rv

def print_matrix(matrix):
    rv = ""
    for i in range(1, 11):
        for j in range(0, 11):
            rv += "%d " % (matrix[(i,j)])

        rv += "\n"
    print rv


def compute_released_dates_difficulties(riotmeta):
    """ Computes the number of champions in each difficulty category """
    difficulties = defaultdict(int)
    released = {}
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

            if not riotmeta or riotmeta in champ_meta:
                difficulties[categorize_diff(int(line['Difficulty']))] += 1
    return released, difficulties

def champion_features(week, riotmeta):
    """ Returns a list of all champions of the given meta and their features for the given week. """
    champions = {}
    with open('../data/all_weeks.csv') as handle:
        reader = csv.DictReader(handle, ['Week', 'Name', 'Difficulty', 'Since', 'Times', 'RiotMeta'])

        for line in reader:
            if int(line['Week']) == int(week):
                name = line['Name']
                difficulty = line['Difficulty']
                since = line['Since']
                times = int(line['Times'])

                champ_meta = line['RiotMeta'].split(':')

                if not riotmeta or riotmeta in champ_meta:
                    champions[name] = {
                        'name': name,
                        'difficulty': difficulty,
                        'since': since,
                        'times': times,
                    }

        return champions

def predict(curr_week, meta):
    curr_week = curr_week - 1

    likelihoods = compute_likelihoods(curr_week, meta)

    #figure out when these doods were released.
    released, difficulties = compute_released_dates_difficulties(meta)

    week_champions = champion_features(curr_week, meta)

    for name in week_champions.keys():
        champ = week_champions[name]
        d = categorize_diff(champ['difficulty'])
        category = categorize_since(int(champ['since']))

        times = champ['times']
        prior = float(times) / (int(curr_week) - released[name])

        num_difficulty = 1
        if d in difficulties:
            num_difficulty = difficulties[d]

        champ['likelihood'] = likelihoods[(d, category)] / num_difficulty
        champ['prior'] = prior

    predictor = lambda x: -(x[1]['likelihood']*x[1]['prior'])
    predictor = lambda x: -(x[1]['prior'])
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
