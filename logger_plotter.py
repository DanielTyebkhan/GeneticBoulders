from MapElites.me_utils import ME_params_to_route

from MapElites.tracking import ExperimentAggregator
from MoonBoardRNN.plotting import plot_route

def plot_agg_routes(agg: ExperimentAggregator):
    for logger in agg.get_loggers():
        archive = logger.archives[-1]
        for elite in archive:
            route = ME_params_to_route([int(i) for i in elite.sol])
            plot_route(route)
