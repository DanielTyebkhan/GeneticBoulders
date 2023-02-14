import os
import ribs
from typing import Any, Callable, Iterable, List, Dict
import statistics
import copy
import numpy as np
import MapElites.visualization as me_viz
from util import split_percentages
from MoonBoardRNN.GradeNet import grade_net
import MapElites.me_utils as me_utils


class ExtendedGridArchive(ribs.archives.GridArchive):
    """
    A subclass of grid archive with useful functions for asking about fitness and qd score
    """
    def __init__(self, dims, ranges, seed=None, dtype=np.float64):
        super().__init__(dims, ranges, seed, dtype)

    def clone(self):
        return copy.deepcopy(self)

    def all_fitnesses(self) -> Iterable[float]:
        return map(ExtendedGridArchive.elite_to_fitness, self)

    def elite_to_fitness(elite):
        return elite.obj

    def elite_to_params(elite):
        return elite.sol

    def __af_map(self, func: Callable[[Iterable[float]], Any]) -> Any:
        return func(self.all_fitnesses())

    def qd_score(self) -> float:
        return self.stats.qd_score

    def max_fitness(self) -> float:
        return self.stats.obj_max

    def min_fitness(self) -> float:
        return self.__af_map(min)

    def average_fitness(self) -> float:
        return self.stats.obj_mean

    def grade_diffs_sum(self) -> float:
        elite_total = sum(me_utils.grade_diff_from_fitness(ExtendedGridArchive.elite_to_fitness(e)) for e in self)
        empty_total = me_utils.NUM_GRADES * (self.bins - len(self))
        return elite_total + empty_total


ArchiveSelector = Callable[[ExtendedGridArchive], float]


class Logger:
    """
    Keeps track of archives over generations
    """
    def __init__(self) -> None:
        self.archives: List[ExtendedGridArchive] = []

    def add_archive(self, archive: ExtendedGridArchive) -> None:
        self.archives.append(archive.clone())

    def gen_qd_score(self, generation: int) -> int:
        return self.archives[generation].qd_score()

    def gen_to_archive(self, generation: int) -> ExtendedGridArchive:
        return self.archives[generation]

    def num_gens(self) -> int:
        return len(self.archives)


Loggers = List[Logger]


class ExperimentAggregator:
    """
    Aggregates loggers from multiple experiments to analyze combined results
    """
    def __init__(self):
        self.__loggers: List[Logger] = []

    def add_logger(self, logger: Logger) -> None:
        self.__loggers.append(logger)

    def __join_data(self, selector: ArchiveSelector) -> List[List[float]]:
        gens = []
        loggers = self.__loggers
        for i in range(loggers[0].num_gens()):
            gen = []
            for logger in self.__loggers:
                gen.append(selector(logger.gen_to_archive(i)))
            gens.append(gen)
        return gens

    def __plot_ranges(self, selector: ArchiveSelector, y_label: str, save_path: os.PathLike, show: bool = False) -> None:
        data = self.__join_data(selector)
        med, p25, p75 = split_percentages(data)
        x_data = list(range(1, len(data) + 1))
        me_viz.plot_ranges(x_coords=x_data, min_vals=p25, mid_vals=med, max_vals=p75,
                           y_label=y_label, x_label='Generation', save_path=save_path, show=show)

    def plot_qd_score(self, save_path: os.PathLike, show: bool=False) -> None:
        self.__plot_ranges(lambda x: x.qd_score(), 'QD Score', save_path, show)

    def plot_max_fitness(self, save_path: os.PathLike, show: bool=False) -> None:
        self.__plot_ranges(lambda x: x.max_fitness(), 'Max Fitness', save_path, show)

    def plot_grade_diffs(self, save_path: os.PathLike, show: bool=False) -> None:
        self.__plot_ranges(lambda x: x.grade_diffs_sum(), 'Target Grade Distance', save_path, show)

    def get_loggers(self):
        return self.__loggers
