import random

from share.moonboard_util import MoonBoardRoute
from MapElites.me_utils import MEParams
import MapElites.ribs_interface as me

def main():
    random.seed(4114)
    params = MEParams(
        (5, 5), [(0, 1), (1, 6)], 50, 0.01, 4, 100)
    me.run_mapelites('V5', params, report_frequency=10)

if __name__ == '__main__':
    main()
