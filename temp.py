import os
from MapElites.tracking import ExperimentAggregator
from util import load_pickle
path = '/home/daniel/GeneticBoulders/results/aggregate.p'

agg: ExperimentAggregator = load_pickle(path)
agg.plot_max_fitness(os.path.join('results', 'fitness.png'), True)
agg.plot_qd_score(os.path.join('results', 'qd.png'), True)
print('')