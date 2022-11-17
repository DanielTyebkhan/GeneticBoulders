import random
from MapElites.tracking import ExperimentAggregator

from share.moonboard_route import MoonBoardRoute
from MapElites.me_utils import MEParams
import MapElites.ribs_interface as me
from util import save_pickle

def main():
    random.seed(4114)
    params = MEParams(
        (6, 6), [(1, 7), (0, 6)], 10, 0.01, 5, 100)
    tasks = 10
    agg = ExperimentAggregator()
    for i in range(5):
        print(f'On experiment {i}')
        agg.add_logger(me.run_mapelites(target_grade='V4', params=params, report_frequency=10, save_path='results'))
    save_pickle(agg, 'results/aggregate.p')

if __name__ == '__main__':
    main()
