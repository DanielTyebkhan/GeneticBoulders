import os
from datetime import datetime

from MapElites.me_utils import MEParams
import MapElites.ribs_interface as me

def main():
    num_reps = 30
    population_size = 25
    num_emitters = 5
    batch_size = population_size // num_emitters
    iterations = 2000
    num_threads = 6
    params = MEParams(
        (3, 4), [(1, 4), (2, 6)], batch_size, num_emitters, iterations)
    # grades = ['V4', 'V5', 'V6', 'V7', 'V8']
    # grades = ['V9', 'V10', 'V11', 'V12', 'V13']
    # grades = ['V6', 'V7', 'V8']
    grades = ['V13']
    for grade in grades:
        start_time = datetime.now()
        print(f'Starting {grade} at {start_time}')
        me.parallel_experiment(grade, params, os.path.join('results', grade), num_reps, num_threads)
        end_time = datetime.now()
        print(f'Finished {grade} at {end_time}')
        print(f'Took {end_time - start_time}')

if __name__ == '__main__':
    main()
