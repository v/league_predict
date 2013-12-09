from examine_data import champions, actual_free, meta_occurrences, meta_count
from sage.all import *
from collections import defaultdict
from itertools import groupby
from pprint import pprint

def posterior(champ, week):
    points = champions[champ]['free_seq']

    #truncate the points after week.
    points = [x for x in points if x[0] < week]

    # only look at the last 5 points.
    points = points[-7:]

    # champion is not released.
    if not points or len(points) < 2:
        return -200

    # replace the zeroth element with enumerate
    fit_points = list(enumerate([x[1] for x in points]))

    var('a,b,t')

    model = symbolic_expression(a*t + b).function(t)

    fit = find_fit(fit_points, model, solution_dict=True)

    tval = len(fit_points)
    aval = fit[a]
    bval = fit[b]

    next_value = aval * tval + bval

    predicted_week = next_value + points[-1][0]

    #if predicted_week < 100:
        #graph1 = scatter_plot(fit_points)
        #graph2 = plot(model.subs(fit), (t, 0, tval))

        #g = graph1 + graph2
        #g.show()
        #import pdb; pdb.set_trace()

    #likelihood = predicted_week - week
    likelihood = abs(predicted_week - week)

    return -1 * likelihood

def matches(actual, predictions):
    mine = set([x[0] for x in predictions])
    yours = set(actual)

    return mine.intersection(yours)

def false_matches(actual, predictions):
    mine = set([x[0] for x in predictions])
    yours = set(actual)

    return mine - yours

def compute_prior(champ_data, week):
    frees = champ_data['free_seq']

    frees = filter(lambda x: x[0] < week, frees)

    num_weeks =  week - champ_data['released']
    if num_weeks == 0:
        num_weeks = 1
    return float(len(frees)) / num_weeks

def compute_meta_factor(champ_data, week):
    sum = 0
    for meta in champ_data['riotmeta']:
        frees = meta_occurrences[meta]
        frees = filter(lambda x: x[0] < week, frees)

        sum += float(len(frees)) / meta_count[meta]
    return sum / len(champ_data['riotmeta'])

def predict(week):

    posteriors = {}
    priors = {}
    meta_factors = {}

    for champ in champions:
        posteriors[champ] = posterior(champ, week)
        priors[champ] = compute_prior(champions[champ], week)
        meta_factors[champ] = compute_meta_factor(champions[champ], week)

    actual = actual_free[week]

    sorted_priors = sorted(priors.iteritems(), key=lambda x: -x[1])
    sorted_posteriors = sorted(posteriors.iteritems(), key=lambda x: -x[1])

    ### Meta ranking stuff

    meta_groups = []
    sorted_metas = sorted(meta_factors.iteritems(), key=lambda x: -x[1])
    for key, group in groupby(sorted_metas, key=lambda x: x[1]):
        meta_groups.append(list(group))

    meta_ranking = {}

    last_rank = 0
    size_last = 0
    for i, group in enumerate(meta_groups):

        for item in group:
            #meta_ranking[item[0]] = last_rank + 1 + size_last
            meta_ranking[item[0]] = last_rank + 1

        last_rank = meta_ranking[group[-1][0]]
        size_last = len(group)

    prior_ranking = dict(map(lambda x: (x[1][0], x[0]), enumerate(sorted_priors)))
    posterior_ranking = dict(map(lambda x: (x[1][0], x[0]), enumerate(sorted_posteriors)))

    avg_ranking = {}

    for champ in champions:
        avg_ranking[champ] = 0.2*prior_ranking[champ] + 0.6*posterior_ranking[champ] + 0.2* meta_ranking[champ]

    predictions = sorted(avg_ranking.iteritems(), key=lambda x: x[1])

    #print week
    #for champ in ['Graves', 'Caitlyn', 'Vayne', 'Sejuani', 'Janna', 'Miss Fortune', 'Sona', 'Nasus', 'Leona', 'Skarner']:
        #print champ, prior_ranking[champ], posterior_ranking[champ], avg_ranking[champ]

    #print week

    #print actual
    #for prediction in predictions[:20]:
        #print prediction

    top_10 = matches(actual, predictions[:10])
    top_20 = matches(actual, predictions[:20])
    top_30 = matches(actual, predictions[:30])

    top_10_misses = set(actual) - top_10
    top_20_misses = set(actual) - top_20
    top_30_misses = set(actual) - top_30

    top_10_false = false_matches(actual, predictions[:10])
    top_20_false = false_matches(actual, predictions[:20])
    top_30_false = false_matches(actual, predictions[:30])

    champ_names = [x[0] for x in predictions]

    return top_10, top_20, top_30, top_10_misses, top_20_misses, top_30_misses, actual, top_10_false, top_20_false, top_30_false, champ_names

def aggregate(champs, result):
    for champ in champs:
        result[champ] += 1

num_weeks = 0

results = [0, 0, 0]

misses = [defaultdict(int), defaultdict(int), defaultdict(int)]
hits = [defaultdict(int), defaultdict(int), defaultdict(int)]
false_champs = [defaultdict(int), defaultdict(int), defaultdict(int)]

occs = defaultdict(int)

predict_count = defaultdict(int)

for week_num in range(100, 200):
    data = predict(week_num)

    print week_num, len(data[0]), len(data[1]), len(data[2])

    results[0] += len(data[0]) / 10.0
    results[1] += len(data[1]) / 10.0
    results[2] += len(data[2]) / 10.0

    aggregate(data[3], misses[0])
    aggregate(data[4], misses[1])
    aggregate(data[5], misses[2])

    aggregate(data[0], hits[0])
    aggregate(data[1], hits[1])
    aggregate(data[2], hits[2])

    aggregate(data[6], occs)

    aggregate(data[7], false_champs[0])
    aggregate(data[8], false_champs[1])
    aggregate(data[9], false_champs[2])

    aggregate(data[10][:10], predict_count)

    num_weeks += 1

print [x / num_weeks for x in results]

sorted_misses = map(lambda x: sorted(x.iteritems(), key=lambda x: -x[1]), misses)
sorted_hits = map(lambda x: sorted(x.iteritems(), key=lambda x: -x[1]), hits)
sorted_occs = sorted(occs.iteritems(), key=lambda x: -x[1])
sorted_false = map(lambda x: sorted(x.iteritems(), key=lambda x: -x[1]), false_champs)

ratios = {}

for champ in champions:
    if predict_count[champ] > 0:
        miss = misses[0][champ] / float(occs[champ])
        hit = hits[0][champ] / float(occs[champ])
        false_occ = false_champs[0][champ] / float(predict_count[champ])


        ratios[champ] = {
            'miss': miss,
            'false': false_occ,
            'hits': hit,
            'occs': occs[champ],
            'predict': predict_count[champ],
        }

sorted_misses = sorted(ratios.iteritems(), key=lambda x: -x[1]['miss'])
sorted_hits = sorted(ratios.iteritems(), key=lambda x: -x[1]['hits'])
sorted_false = sorted(ratios.iteritems(), key=lambda x: -x[1]['false'])

print "Misses:"
#print sorted_misses[0][:10]
#print sorted_misses[1][:10]
#print sorted_misses[2][:10]
for item in sorted_misses[:10]:
    print '\t', item[0], item[1]['miss'], item[1]['predict'], item[1]['occs']

print "Hits:"
#print sorted_hits[0][:10]
#print sorted_hits[1][:10]
#print sorted_hits[2][:10]
for item in sorted_hits[:10]:
    print '\t', item[0], item[1]['hits'], item[1]['predict'], item[1]['occs']

print "False:"
#print sorted_false[0][:10]
#print sorted_false[1][:10]
#print sorted_false[2][:10]
for item in sorted_false[:10]:
    print '\t', item[0], item[1]['false'], item[1]['predict']

print "Occurrences:"
print sorted_occs

import pdb; pdb.set_trace()

#points = list(enumerate(free_data['Janna']))

#var('a, b, t')
#model(t) = a * (t) + b
#fit = find_fit(points, model, solution_dict=True)

#graph1 = plot(model.subs(fit), (t, 0, 60))
#graph2 = scatter_plot(points)

#graph = graph1 + graph2

#graph.show()
#import pdb; pdb.set_trace()
