
import os
from MapElites.me_utils import MEParams
import MapElites.ribs_interface as me
from util import save_pickle

def main():
    # random.seed(4114)
    params = MEParams(
        (6, 6), [(1, 7), (0, 6)], 10, 0.01, 5, 100)
    grades = ['V4', 'V6', 'V8', 'V9']
    for grade in grades:
        me.parallel_experiment(grade, params, os.path.join('results', grade), 30, 6)

if __name__ == '__main__':
    main()
