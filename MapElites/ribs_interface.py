import os
import time
import matplotlib.pyplot as plt
import ribs
import ribs.visualize
from MoonBoardRNN.GradeNet.grade_net import GradeNet
from share.moonboard_util import MoonBoardRoute
from MapElites.me_utils import MEParams, get_me_params_bounds, route_to_ME_params, ME_params_to_route
import util


def grade_string_to_num(grade: str) -> int:
    return int(grade[1:])


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
            bounds=input_bounds
        ) for i in range(params.num_emitters)
    ]
    optimizer = ribs.optimizers.Optimizer(archive, emitters)
    start_time = time.time()
    for itr in range(1, params.iterations + 1):
        print(f'Starting ask at {time.time()}')
        population = optimizer.ask()
        print(f'Finished ask at {time.time()}')
        objc, bcs = [], []
        for individual in population:
            route = ME_params_to_route(individual)
            rating = 'V10000000' if not route.is_valid() else gradenet.grade_route(route)
            hold_variety = route.get_hold_variety()
            hold_density = route.get_hold_density()
            fitness = abs(target - grade_string_to_num(rating))
            objc.append(fitness)
            bcs.append([hold_variety, hold_density])

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
    plot_path = os.path.join(output_dir, 'archive.png')
    ribs.visualize.grid_archive_heatmap(archive)
    plt.show()
    plt.savefig(plot_path)



