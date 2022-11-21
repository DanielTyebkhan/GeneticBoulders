import os
from MapElites.me_utils import MEParams
import MapElites.ribs_interface as me

def main():
    num_reps = 6
    ind_per_emitter = 2
    iterations = 10
    params = MEParams(
        (6, 6), [(1, 7), (0, 6)], ind_per_emitter, 0.01, 5, iterations)
    grades = ['V4', 'V6', 'V8', 'V9']
    for grade in grades:
        me.parallel_experiment(grade, params, os.path.join('results', grade), num_reps, 6)

if __name__ == '__main__':
    main()
