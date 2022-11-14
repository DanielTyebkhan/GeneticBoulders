import copy
import os
from statistics import mean, median
import time
from typing import List
import matplotlib.pyplot as plt
import ribs
import ribs.visualize
from MoonBoardRNN.GradeNet.grade_net import GradeNet
from share.moonboard_route import MoonBoardRoute
from MapElites.me_utils import MEParams, get_me_params_bounds, route_to_ME_params, ME_params_to_route
import util

class ExtendedGridArchive(ribs.archives.GridArchive):
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

    def average_fitness(self):
        return self.__af_map(mean)


class Logger:
    def __init__(self) -> None:
        self.archives: List[List[ExtendedGridArchive]] = []

    def add_archive(self, generation: int, archive: ExtendedGridArchive):
        self.archives[generation].append(archive.clone())
    
    def gen_qd_score(self, generation: int) -> int:
        return 0

    def gen_to_archives(self, generation: int) -> ExtendedGridArchive:
        return self.archives[generation]


def grade_string_to_num(grade: str) -> int:
    return int(grade[1:])


def eval_fitness(route: MoonBoardRoute, target_grade: int, gradenet: GradeNet):
    # TODO: figure out why we sometimes get a key error
    fitness = -1
    try:
        if route.is_valid():
            grade = gradenet.grade_route(route)
            num_grade = grade_string_to_num(grade)
            diff = abs(target_grade - num_grade)
            if diff == 0:
                fitness = 1
            else:
                fitness = 1/diff
    except Exception as ex:
        fitness = 0
    return fitness


def run_mapelites(*, target_grade: str, params: MEParams, save_path: str, report_frequency: int=25):
    target = grade_string_to_num(target_grade)
    gradenet = GradeNet()
    archive = ribs.archives.GridArchive(params.grid_size, params.bounds)
    input_bounds = get_me_params_bounds()
    initial_routes = [MoonBoardRoute.make_random_valid()] * params.num_emitters
    x0s = [route_to_ME_params(r) for r in initial_routes]
    emitters = [
        ribs.emitters.ImprovementEmitter(
            archive=archive, 
            x0=x0s[i],
            sigma0=params.sigma_0,
            batch_size=params.batch_size,
            bounds=input_bounds,
            restart_rule='basic'
        ) for i in range(params.num_emitters)
    ]
    optimizer = ribs.optimizers.Optimizer(archive, emitters)
    start_time = time.time()
    for itr in range(1, params.iterations + 1):
        population = optimizer.ask()
        objc, bcs = [], []
        for individual in population:
            route = ME_params_to_route(individual)
            fitness = eval_fitness(route, target, gradenet)
            hold_variety = route.get_hold_variety()
            hold_density = route.get_hold_density()
            if hold_variety in [1, 4] and (hold_density < 0.4 or hold_density > 0.8):
                hold_density = 0.5
                hold_density = 3
            objc.append(fitness)
            bcs.append([hold_density, hold_variety])

        optimizer.tell(objc, bcs)

        if itr % report_frequency == 0:
            elapsed_time = time.time() - start_time
            print(f"> {itr} itrs completed after {elapsed_time:.2f} s")
            print(f"  - Archive Size: {len(archive)}")
            print(f"  - Max Score: {archive.stats.obj_max}")
    
    output_dir = os.path.join(save_path, str(time.time()))
    os.makedirs(output_dir, exist_ok=True)
    pickle_path = os.path.join(output_dir, 'archive.p')
    util.save_pickle(archive, pickle_path)
    viz_archive(archive, output_dir)



def viz_archive(archive, output_dir):
    plot_archive_heatmap(archive, os.path.join(output_dir, 'archive.png'))
    # draw_archive_on_board(archive, os.path.join(output_dir, 'board_images'))

def plot_archive_heatmap(archive, save_path):
    plt.ylabel('Hold Diversity')
    plt.xlabel('Hold Density')
    ribs.visualize.grid_archive_heatmap(archive)
    plt.savefig(save_path)
    plt.show()

def draw_archive_on_board(archive: ribs.archives.GridArchive, save_path):
    for elite in archive:
        print(elite)
    


