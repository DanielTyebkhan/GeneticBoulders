import random

from share.moonboard_util import MoonBoardRoute
from MapElites.me_utils import MEParams
import MapElites.ribs_interface as me

def main():
    random.seed(4114)
    params = MEParams(
        (5, 4), [(0, 1), (1, 5)], 50, 0.01, 4, 500)
    me.run_mapelites('V5', params)

if __name__ == '__main__':
    main()
