import random

from share.moonboard_route import MoonBoardRoute
from MapElites.me_utils import MEParams
import MapElites.ribs_interface as me

def main():
    random.seed(4114)
    params = MEParams(
        (6, 6), [(1, 7), (0, 6)], 50, 0.01, 4, 200)
    for i in range(3):
        print(f'On experiment {i}')
        me.run_mapelites(target_grade='V4', params=params, report_frequency=10, save_path='results')

if __name__ == '__main__':
    main()
