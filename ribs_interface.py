import time
import ribs
import structs
import simulator_interface

# TODO: add seed
def run_mapelites(params: structs.MEParams, report_frequency: int=25):
    sim_params = None
    archive = ribs.archives.GridArchive(params.grid_size, params.bounds)
    emitters = [
        ribs.emitters.ImprovementEmitter(
            archive, 
            structs.MoonBoardRoute.randomize(),
            params.sigma_0,
            params.batch_size) for _ in range(params.num_emitters)
    ]
    optimizer = ribs.optimizers.Optimizer(archive, emitters)
    start_time = time.time()
    for itr in range(1, params.iterations):
        population = optimizer.ask()
        objc, bcs = [], []
        for individual in population:
            work_done, hold_variety, hold_density = simulator_interface.run_simulation(individual, sim_params)
            objc.append(work_done)
            bcs.append([hold_variety, hold_density])

        optimizer.tell(objc, bcs)

        if itr % report_frequency == 0:
            elapsed_time = time.time() - start_time
            print(f"> {itr} itrs completed after {elapsed_time:.2f} s")
            print(f"  - Archive Size: {len(archive)}")
            print(f"  - Max Score: {archive.stats.obj_max}")

        

