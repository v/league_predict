import sys
from collections import defaultdict
from pprint import pprint

from util import champion_features, compute_likelihoods, compute_released_dates_difficulties, categorize_diff, categorize_since, predict, get_free_champs

METAS = ['top', 'mid', 'jungle', 'adc', 'support']

free_champ_data = get_free_champs()

def matches(predictions, actual):
    champs = [prediction[0] for prediction in predictions]

    return set(actual).intersection(set(champs))

def compute_week(week):
    actual_champs = free_champ_data[week]

    top_10 = []
    top_20 = []
    top_30 = []

    for meta in METAS:
        predictions = predict(week, meta)

        top_10 += predictions[:2]
        top_20 += predictions[:4]
        top_30 += predictions[:6]


    ten = matches(top_10, actual_champs)
    twenty = matches(top_20, actual_champs)
    thirty = matches(top_30, actual_champs)

    #predictions = predict(week, None)

    #ten = matches(predictions[:10], actual_champs)
    #twenty = matches(predictions[:20], actual_champs)
    #thirty = matches(predictions[:30], actual_champs)

    return ten, twenty, thirty

if __name__ == '__main__':
    num_weeks = 0

    sums = [0, 0, 0, 0]
    for week in range(100, 203):
        ten, twenty, thirty, all = compute_week(week)

        sums[0] += len(ten)
        sums[1] += len(twenty)
        sums[2] += len(thirty)

        print num_weeks, [len(ten), len(twenty), len(thirty)], ten

        num_weeks += 1

    print [x / (num_weeks * 10.0) for x in sums]
