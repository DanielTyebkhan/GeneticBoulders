from MapElites.me_utils import ME_params_to_route, grade_diff_from_fitness

from MapElites.tracking import ExperimentAggregator, ExtendedGridArchive
from MoonBoardRNN.plotting import plot_route

def plot_agg_routes(agg: ExperimentAggregator, only_target: bool=False, save_path=None):
    for logger in agg.get_loggers():
        archive = logger.archives[-1]
        for elite in archive:
            plot = True
            if only_target:
                if grade_diff_from_fitness(ExtendedGridArchive.elite_to_fitness(elite)) > 0:
                    plot = False
            if plot:
                route = ME_params_to_route([int(i) for i in elite.sol])
                plot_route(route, save_path=save_path)
