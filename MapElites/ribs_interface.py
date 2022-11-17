from threading import Thread
import os
from statistics import mean, median
import time
from typing import Dict, List
import matplotlib.pyplot as plt
import ribs
import ribs.visualize
from MoonBoardRNN.GradeNet.grade_net import GradeNet
from MoonBoardRNN.BetaMove.BetaMove import load_feature_dict
from share.moonboard_route import MoonBoardRoute
from MapElites.me_utils import MEParams, get_me_params_bounds, route_to_ME_params, ME_params_to_route
import util
from tracking import ExtendedGridArchive, Logger


def grade_string_to_num(grade: str) -> int:
    return int(grade[1:])


def eval_fitness(route: MoonBoardRoute, target_grade: int, gradenet: GradeNet, feature_dict=None):
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
    logger = Logger()
    target = grade_string_to_num(target_grade)
    gradenet = GradeNet()
    archive = ExtendedGridArchive(params.grid_size, params.bounds)
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
    feature_dict = load_feature_dict()
    start_time = time.time()
    for itr in range(1, params.iterations + 1):
        population = optimizer.ask()
        objc, bcs = [], []
        for individual in population:
            route = ME_params_to_route(individual)
            fitness = eval_fitness(route, target, gradenet, feature_dict)
            hold_variety = route.get_hold_variety()
            max_span = route.get_max_span()
            objc.append(fitness)
            bcs.append([max_span, hold_variety])

        optimizer.tell(objc, bcs)
        logger.add_archive(itr, archive)

        if itr % report_frequency == 0:
            elapsed_time = time.time() - start_time
            print(f"> {itr} itrs completed after {elapsed_time:.2f} s")
            print(f"  - Archive Size: {len(archive)}")
            print(f"  - Max Score: {archive.stats.obj_max}")
    
    output_dir = os.path.join(save_path, str(time.time()))
    os.makedirs(output_dir, exist_ok=True)
    archive_pickle_path = os.path.join(output_dir, 'archive.p')
    logger_pickle_path = os.path.join(output_dir, 'logger.p')
    util.save_pickle(archive, archive_pickle_path)
    util.save_pickle(logger, logger_pickle_path)
    # viz_archive(archive, output_dir)
    return logger

def thread_target(queue):
    task = queue.get()


def parallel_experiment(target_grade, params, save_path, report_frequency=25, num_threads=4):
    thread_target = lambda: run_mapelites(target_grade=target_grade, params=params, save_path=save_path, report_frequency=report_frequency)
    workers = [Thread(target=thread_target)]


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
    


