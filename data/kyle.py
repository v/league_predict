import csv
from collections import defaultdict
from dateutil.parser import parse
from pprint import pprint

def percent(input):
    "10% == 0.1"
    return float(input.strip('%'))/100

champions = {}
with open('champions.csv') as handle:
    reader = csv.DictReader(handle, ['Name', 'RP', 'IP', 'Popularity', 'Win Rate', 'Ban Rate', 'Meta', 'Released', 'Difficulty'])

    i = 0

    for line in reader:
        if i == 0:
            i += 1
            continue
        name = line['Name']
        ip = line['IP']
        popularity = percent(line['Popularity'])
        ban_rate = percent(line['Ban Rate'])
        released = parse(line['Released'])
        difficulty = line['Difficulty']

        champions[name] = {
            'name': name,
            'ip': ip,
            'popularity': popularity,
            'ban_rate': ban_rate,
            'released': released,
            'difficulty': difficulty,
            'last_free': 0,
            'times_free': 0,
        }

def released(date, champ):
    return champ['released'] < date

free_champ_data = []

with open('free_week.csv') as handle:
    reader = csv.reader(handle, delimiter=',', quotechar='"')

    for line in reader:
        date = parse(line[0])
        free_champs = line[1:]

        free_champ_data.append(free_champs)

def next_free(week_num, champ):
    curr = week_num + 1

    while curr < len(free_champ_data):
        if champ in free_champ_data[curr]:
            return curr - week_num
        curr += 1

    return curr - week_num

with open('free_week.csv') as handle:
    reader = csv.reader(handle, delimiter=',', quotechar='"')

    week_num = 0

    for line in reader:
        date = parse(line[0])
        free_champs = line[1:]

        # print em out.
        for name in champions.keys():
            champ = champions[name]

            weeks_since_free = week_num - champ['last_free']
            if champ['name'] in free_champs:
                champ['last_free'] = week_num
                champ['times_free'] += 1

            if released(date, champ) and champ['name'] in free_champs:
                csv_data = [
                    #str(next_free(week_num, champ['name'])),
                    str(champ['difficulty']),
                    str(weeks_since_free),
                    str(champ['times_free']),
                ]

                print ','.join(csv_data)

        week_num += 1
