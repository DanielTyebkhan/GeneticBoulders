# import os
# from MapElites.tracking import ExperimentAggregator
# from util import load_pickle
# from MoonBoardRNN.plotting import plot_route
# from MapElites.me_utils import ME_params_to_route
# archives = [
#         '/home/daniel/GeneticBoulders/results/1668706120.819965/archive.p',
#         '/home/daniel/GeneticBoulders/results/1668707131.2126865/archive.p',
#         '/home/daniel/GeneticBoulders/results/1668708277.0423818/archive.p',
#         '/home/daniel/GeneticBoulders/results/1668709058.825623/archive.p',
#         '/home/daniel/GeneticBoulders/results/1668709810.6575437/archive.p'
#         ]

# savepath = '/home/daniel/Desktop/route_images'
# for i, path in enumerate(archives):
#     archive = load_pickle(path)
#     for j, elite in enumerate(archive):
#         plot_route(ME_params_to_route(elite.sol), os.path.join(savepath, f'{str(i)}_{str(j)}.jpg'))
    

from util import load_pickle

path = '/home/tyebkhad/GeneticBoulders/results/V5Exp/aggregator.p'
agg = load_pickle(path)
print('')