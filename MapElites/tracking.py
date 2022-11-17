import ribs
from collections import defaultdict
from typing import List, Dict
import statistics
import copy
import numpy as np

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


class Logger:
    def __init__(self) -> None:
        self.archives: Dict[int, List[ExtendedGridArchive]] = defaultdict(list)

    def add_archive(self, generation: int, archive: ExtendedGridArchive):
        self.archives[generation].append(archive.clone())
    
    def gen_qd_score(self, generation: int) -> int:
        return 0

    def gen_to_archives(self, generation: int) -> ExtendedGridArchive:
        return self.archives[generation]