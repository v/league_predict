""" This file makes a CSV that has data about champion features anytime they are free """
import csv
from dateutil.parser import parse
from collections import defaultdict

with open('../data/champions.csv') as handle:
    reader = csv.DictReader(handle, ['Name', 'RP', 'IP', 'Popularity', 'Win Rate', 'Ban Rate', 'Meta', 'Released', 'Difficulty', 'RiotMeta'])

    i = 0

    champions = {}

    for line in reader:
        if i == 0:
            i += 1
            continue
        name = line['Name']
        ip = line['IP']
        released = parse(line['Released'])
        difficulty = int(line['Difficulty'])
        riotmeta = line['RiotMeta'].split(':')

        champions[name] = {
            'name': name,
            'ip': ip,
            'released': released,
            'difficulty': difficulty,
            'last_free': 0,
            'times_free': 0,
            'riotmeta': riotmeta,
        }


with open('../data/free_week.csv') as handle:
    reader = csv.reader(handle, delimiter=',', quotechar='"')

    free_data = defaultdict(list)
    last_free = defaultdict(int)

    week_num = 0

    for line in reader:
        date = parse(line[0])
        free_champs = line[1:]

        for champ in free_champs:

            weeks_since = week_num - last_free[champ]

            if weeks_since == 1:
                print week_num, champ

            #free_data[champ].append(weeks_since)
            free_data[champions[champ]['difficulty']].append(weeks_since)
            last_free[champ] = week_num

        week_num += 1

    for i in range(1, 11):
        print i, free_data[i]
        print ""
