import os
import ribs
from typing import Callable, List, Dict
import statistics
import copy
import numpy as np
import MapElites.visualization as me_viz
from util import split_percentages


class ExtendedGridArchive(ribs.archives.GridArchive):
    def __init__(self, dims, ranges, seed=None, dtype=np.float64):
        super().__init__(dims, ranges, seed, dtype)

    def clone(self):
        return copy.deepcopy(self)

    def all_fitnesses(self):
        return map(lambda x: x.obj, self)

    def __af_map(self, func):
        return func(self.all_fitnesses())

    def qd_score(self):
        return self.__af_map(sum)

    def max_fitness(self):
        return self.__af_map(max)

    def min_fitness(self):
        return self.__af_map(min)

    def average_fitness(self):
        return self.__af_map(statistics.mean)


ArchiveSelector = Callable[[ExtendedGridArchive], float]


class Logger:
    def __init__(self) -> None:
        self.archives: List[ExtendedGridArchive]

    def add_archive(self, generation: int, archive: ExtendedGridArchive):
        self.archives.append(archive.clone())

    def gen_qd_score(self, generation: int) -> int:
        return 0

    def gen_to_archive(self, generation: int) -> ExtendedGridArchive:
        return self.archives[generation]

    def num_gens(self):
        return len(self.archives)

    def __join_data(self, selector: ArchiveSelector):
        data = []
        for i in len(self.archives):
            data.append[[selector(e) for e in self.archives[i]]]
        return data

    def __plot_ranges(self, selector: ArchiveSelector, y_label: str, save_path: os.PathLike, show: bool = False):
        data = self.__join_data(ArchiveSelector)
        med, p25, p75 = split_percentages(data)
        plot_ranges(x_coords=list(range(1, len(self.archives) + 1)), min_vals=p25, mid_vals=med,
                    max_vals=p75, x_label='Generation', y_label=y_label, save_path=save_path, show=show)

    def plot_max_fit(self, save_path: os.PathLike, show: bool = False):
        self.__plot_ranges(lambda x: x.max_fitness(),
                           'Max Fitness', save_path, show)

    def plot_qd_score(self, save_path: os.PathLike, show: bool = False):
        self.__plot_ranges(lambda x: x.qd_score(), 'QD Score', save_path, show)


Loggers = List[Logger]


class ExperimentAggregator:
    def __init__(self) -> None:
        self.__loggers: List[Logger] = []

    def add_logger(self, logger: Logger):
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

    def __plot_ranges(self, selector: ArchiveSelector, y_label: str, save_path: os.PathLike, show: bool = False):
        data = self.__join_data(selector)
        all_mid, all_p25, all_p75 = [], [], []
        for gen in data:
            mid, p25, p75 = split_percentages(gen)
            all_mid.append(mid)
            all_p25.append(p25)
            all_p75.append(p75)
        x_data = list(range(1, len(data) + 1))
        me_viz.plot_ranges(x_coords=x_data, min_vals=all_p25, mid_vals=all_mid, max_vals=all_p75,
                           y_label=y_label, x_label='Generation', save_path=save_path, show=show)

    def plot_qd_score(self, save_path: os.PathLike, show: bool=False):
        self.__plot_ranges(lambda x: x.qd_score(), 'QD Score', save_path, show)

    def plot_max_fitness(self, save_path: os.PathLike, show: bool=False):
        self.__plot_ranges(lambda x: x.max_fitness(), 'QD Score', save_path, show)
