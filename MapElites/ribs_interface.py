import time
import ribs
from MoonBoardRNN.GradeNet.grade_net import GradeNet
from share.moonboard_util import MoonBoardRoute
from MapElites.me_utils import MEParams, get_me_params_bounds, route_to_ME_params, ME_params_to_route

def grade_string_to_num(grade: str) -> int:
    return int(grade[1:])

def run_mapelites(target_grade: str, params: MEParams, report_frequency: int=25):
    target = grade_string_to_num(target_grade)
    gradenet = GradeNet()
    archive = ribs.archives.GridArchive(params.grid_size, params.bounds)
    input_bounds = get_me_params_bounds()
    emitters = [
        ribs.emitters.ImprovementEmitter(
            archive, 
            route_to_ME_params(MoonBoardRoute.make_random_valid()),
            params.sigma_0,
            params.batch_size,
            bounds=input_bounds
        ) for _ in range(params.num_emitters)
    ]
    optimizer = ribs.optimizers.Optimizer(archive, emitters)
    start_time = time.time()
    for itr in range(1, params.iterations):
        population = optimizer.ask()
        objc, bcs = [], []
        for individual in population:
            route = ME_params_to_route(individual)
            rating = gradenet.grade_route(route)
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

