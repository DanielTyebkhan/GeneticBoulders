import multiprocessing as mp
import os
import time
from typing import Iterable, List
import matplotlib.pyplot as plt
import ribs
import ribs.visualize
from MoonBoardRNN.GradeNet.grade_net import GradeNet
from MoonBoardRNN.BetaMove.BetaMove import load_feature_dict
from share.moonboard_route import MoonBoardRoute
from MapElites.me_utils import MEParams, grade_string_to_num, route_to_ME_params, ME_params_to_route
from share.moonboard_util import END_HOLDS, MAX_MID_HOLDS, MID_HOLDS, MIN_MID_HOLDS, START_HOLDS
import util
from MapElites.tracking import ExperimentAggregator, ExtendedGridArchive, Logger

import random

class RandomEmitter(ribs.emitters.EmitterBase):
    """
    Baseline Emitter --> Just makes random routes for ask()
    """

    def __init__(self, archive: ribs.archives.ArchiveBase, batch_size: int):
        """
        archive: the associated archive
        option_pool: the pool of possible elements of an elite
        batch_size: the number of elites to ask and tell
        """
        super().__init__(archive, len(RandomEmitter.__make_elite()), None)
        self.__batch_size = batch_size

    def __make_elite():
        return route_to_ME_params(MoonBoardRoute.make_random_valid())
 
    def ask(self) -> List[List[int]]:
        return [RandomEmitter.__make_elite() for i in range(self.__batch_size)]
            
    def tell(self, solutions: List[List[float]], objective_values: List[float], behavior_values: List[List[float]], metadata=None) -> None:
        for elite, fitness, behavior in zip(solutions, objective_values, behavior_values):
            self.archive.add(elite, fitness, behavior)

class DiscreteKSwapsEmitter(ribs.emitters.EmitterBase):
    """
    Derived from 
        Mapping Hearthstone Deck Spaces through MAP-Elites with Sliding Boundaries
        Fontaine et al
        https://arxiv.org/pdf/1904.10656v1.pdf
    """

    def __init__(self, archive: ribs.archives.ArchiveBase, initial_elite: List[int], option_pools: List[List[int]], batch_size: int):
        """
        archive: the associated archive
        initial_solution: the initial solution to start from
        option_pool: the pool of possible elements of an elite
        batch_size: the number of elites to ask and tell
        """
        assert len(initial_elite) == len(option_pools)
        super().__init__(archive, len(initial_elite), None)
        self.__initial_elite = initial_elite
        self.__option_pools = [set(p) for p in option_pools]
        self.__batch_size = batch_size
        self.__first_ask = True

    def __pick_k(self) -> int:
        """
        P(k) = 0.5 * P(k-1)
        P(1) = 0.5
        """
        k_offset = 5
        while True:
            r = random.random()
            k = 1 + k_offset
            while r < 0.5 ** (k - k_offset):
                k += 1
            if k < self.solution_dim:
                break
        return k

    def __select_elite(self) -> List[int]:
        sol, _, _, *_ = self.archive.get_random_elite()
        return [int(i) for i in sol]

    def __mutated_elite(self, elite) -> List[int]:
        """
        does not mutate input, returns new mutated form
        """
        k = self.__pick_k()
        to_replace = set(random.choices(range(len(elite)), k=k))
        new_elite = []
        for i, entry in enumerate(elite):
            if i in to_replace:
                used_holds = set(elite + new_elite).difference([-1])
                options = self.__option_pools[i]
                possible_values = options.difference(used_holds)
                value = random.choice(list(possible_values))
            else:
                value = entry
            new_elite.append(value)
        return new_elite
 
    def ask(self) -> List[List[int]]:
        batch_size = self.__batch_size
        if self.__first_ask:
            self.__first_ask = False
            elites = [self.__initial_elite for _ in range(batch_size)]
        else:
            elites = [self.__select_elite() for _ in range(batch_size)]
        return [self.__mutated_elite(e) for e in elites]
            
    def tell(self, solutions: List[List[float]], objective_values: List[float], behavior_values: List[List[float]], metadata=None) -> None:
        for elite, fitness, behavior in zip(solutions, objective_values, behavior_values):
            self.archive.add(elite, fitness, behavior)
        


def eval_fitness(route: MoonBoardRoute, target_grade: int, gradenet: GradeNet, feature_dict=None) -> float:
    fitness = 0
    try:
        if route.is_valid():
            route.purge_holds(feature_dict)
            grade = gradenet.grade_route(route, feature_dict)
            num_grade = grade_string_to_num(grade)
            g_diff = abs(target_grade - num_grade)
            holds = route.num_holds()
            score = g_diff + holds * 0.01
            fitness = 1 / score
    except Exception as ex:
        print(f'Exception evaluating fitness {ex}')
        fitness = 0
    return fitness


def run_mapelites(*, target_grade: str, params: MEParams, save_path: str, report_frequency: int=25) -> Logger:
    logger = Logger()
    target = grade_string_to_num(target_grade)
    gradenet = GradeNet()
    archive = ExtendedGridArchive(params.grid_size, params.bounds)
    initial_routes = [MoonBoardRoute.make_random_valid() for _ in range(params.num_emitters)]
    x0s = [route_to_ME_params(r) for r in initial_routes ]
    start_indices = [MoonBoardRoute.hold_to_valid_index(h) for h in START_HOLDS]
    end_indices = [MoonBoardRoute.hold_to_valid_index(h) for h in END_HOLDS]
    mid_indices = [MoonBoardRoute.hold_to_valid_index(h) for h in MID_HOLDS]
    option_pools = [start_indices, end_indices] + [mid_indices + [-1] for _ in range(MAX_MID_HOLDS)]
    emitters = [DiscreteKSwapsEmitter(
        archive=archive,
        initial_elite=x0s[i],
        option_pools=option_pools,
        batch_size=params.batch_size
    ) for i in range(params.num_emitters)]
    optimizer = ribs.optimizers.Optimizer(archive, emitters)
    feature_dict = load_feature_dict()
    start_time = time.time()
    for itr in range(1, params.iterations + 1):
        population = optimizer.ask()
        objc, bcs = [], []
        for ind, individual in enumerate(population):
            print(f'{itr}: evaluating individual {ind+1}', end='\r')
            route = ME_params_to_route(individual)
            fitness = eval_fitness(route, target, gradenet, feature_dict)
            hold_variety = route.get_hold_variety()
            max_span = route.get_max_span(feature_dict)
            objc.append(fitness)
            bcs.append([hold_variety, max_span])
        print('')

        optimizer.tell(objc, bcs)
        logger.add_archive(archive)

        if itr % report_frequency == 0:
            elapsed_time = time.time() - start_time
            print(f"> {itr} itrs completed after {elapsed_time:.2f} s")
            print(f"  - Archive Size: {len(archive)}")
            print(f"  -    Max Score: {archive.stats.obj_max}")
            print(f"  -     QD Score: {archive.qd_score()}")
    
    output_dir = os.path.join(save_path, str(time.time()))
    os.makedirs(output_dir, exist_ok=True)
    archive_pickle_path = os.path.join(output_dir, 'archive.p')
    logger_pickle_path = os.path.join(output_dir, 'logger.p')
    util.save_pickle(archive, archive_pickle_path)
    util.save_pickle(logger, logger_pickle_path)
    return logger

def __thread_target(target_grade, params, save_path, report_frequency) -> List[Logger]:
    logger = run_mapelites(target_grade=target_grade, params=params, save_path=save_path, report_frequency=report_frequency)
    return logger

def parallel_experiment(target_grade: str, params: MEParams, output_dir: os.PathLike, num_runs: int, num_threads: int, report_frequency: int=25):
    os.makedirs(output_dir, exist_ok=True)
    with mp.Pool(num_threads) as pool:
        loggers = pool.starmap(__thread_target, [(target_grade, params, output_dir, report_frequency)] * num_runs)
    aggregator = ExperimentAggregator()
    for logger in loggers:
        aggregator.add_logger(logger)
    util.save_pickle(aggregator, os.path.join(output_dir, 'aggregator.p'))
    util.save_pickle(params, os.path.join(output_dir, 'me_params.p'))
    return aggregator


def viz_archive(archive, output_dir):
    plot_archive_heatmap(archive, os.path.join(output_dir, 'archive.png'))
    # draw_archive_on_board(archive, os.path.join(output_dir, 'board_images'))

def plot_archive_heatmap(archive, save_path):
    plt.ylabel('Hold Diversity')
    plt.xlabel('Max Span')
    ribs.visualize.grid_archive_heatmap(archive)
    plt.savefig(save_path)

def draw_archive_on_board(archive: ribs.archives.GridArchive, save_path):
    for elite in archive:
        print(elite)
    


