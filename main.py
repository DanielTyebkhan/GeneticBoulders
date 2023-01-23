import os
from MapElites.me_utils import MEParams
import MapElites.ribs_interface as me

def main():
    num_reps = 30
    population_size = 50
    num_emitters = 5
    batch_size = population_size // num_emitters
    iterations = 300
    params = MEParams(
        (3, 4), [(1, 4), (2, 6)], batch_size, num_emitters, iterations)
    grades = ['V4', 'V6', 'V8', 'V9']
    for grade in grades:
        me.parallel_experiment(grade, params, os.path.join('results', grade), num_reps, 6)

if __name__ == '__main__':
    main()
