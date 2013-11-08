from examine_data import champions, actual_free
from sage.all import *


def posterior(champ, week):
    points = champions[champ]['free_seq']

    #truncate the points after week.
    points = [x for x in points if x[0] < week]

    # truncate points before week 50.
    # points = [x for x in points if x[0] >= 50]

    # champion is not released.
    if not points or len(points) < 2:
        return 200

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
    prior = float(champions[champ]['times_free']) / week

    return likelihood

def matches(actual, predictions):
    mine = set([x[0] for x in predictions])
    yours = set(actual)

    return mine.intersection(yours)

def predict(week):

    posteriors = {}

    for champ in champions:
        posteriors[champ] = posterior(champ, week)

    actual = actual_free[week]

    predictions = sorted(posteriors.iteritems(), key=lambda x: x[1])

    top_10 = matches(actual, predictions[:10])
    top_20 = matches(actual, predictions[:20])
    top_30 = matches(actual, predictions[:30])

    return top_10, top_20, top_30

champion = 'Ashe'
week_num = 150
num_weeks = 0

results = [0, 0, 0]

for week_num in range(100, 200):
    data = predict(week_num)

    print week_num, len(data[0]), len(data[1]), len(data[2])

    results[0] += len(data[0]) / 10.0
    results[1] += len(data[1]) / 10.0
    results[2] += len(data[2]) / 10.0

    num_weeks += 1

print [x / num_weeks for x in results]


#points = list(enumerate(free_data['Janna']))

#var('a, b, t')
#model(t) = a * (t) + b
#fit = find_fit(points, model, solution_dict=True)

#graph1 = plot(model.subs(fit), (t, 0, 60))
#graph2 = scatter_plot(points)

#graph = graph1 + graph2

#graph.show()
#import pdb; pdb.set_trace()
