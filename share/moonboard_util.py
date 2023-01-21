from math import sqrt
from typing import Dict, List
from dataclasses import dataclass
import util
from csv import DictReader



def moonboard_row_to_index(row: int) -> int:
    return row - 1


def moonboard_col_to_index(col: str) -> int:
    return ord(col) - util.A_OFFSET


@dataclass(frozen=True)
class MoonBoardHold:
    row: int
    col: int

    def from_string(coords: str):
        return MoonBoardHold(row=moonboard_row_to_index(int(coords[1:])), col=moonboard_col_to_index(coords[0]))

    def from_string_list(strlist: List[str]):
        return [MoonBoardHold.from_string(s) for s in strlist]

    def to_coordinate_string(self) -> str:
        return chr(util.A_OFFSET + self.col) + str(self.row + 1)

    def from_xy(x, y):
        return MoonBoardHold(row=y, col=x)

    def from_beta_vector(beta_vec):
        return MoonBoardHold.from_xy(int(beta_vec[6]), int(beta_vec[7]))


MoonBoardHolds = List[MoonBoardHold]

def load_hold_types(path: str) -> Dict[MoonBoardHold, int]:
    '''
    1 = small crimp
    2 = large crimp
    3 = small pinch
    4 = large pinch
    5 = small pocket
    6 = large pocket
    '''
    hold_categories = {
        1: 'crimp',
        2: 'crimp',
        3: 'pinch',
        4: 'pinch',
        5: 'pocket',
        6: 'pocket'
    }
    types = {}
    with open(path, 'r') as file:
        reader = DictReader(file, ['x', 'y', 'val'])
        next(reader)
        for row in reader:
            types[(MoonBoardHold(int(row['y']), int(row['x'])))] = hold_categories[int(row['val'])]
    return types




COLUMNS = 11
ROWS = 18
MAX_START_ROW = 5  # 0 based indexing

# TODO: increase maxes to 2
MIN_START_HOLDS = 1
MAX_START_HOLDS = 1
MIN_END_HOLDS = 1
MAX_END_HOLDS = 1
MIN_MID_HOLDS = 4
MAX_MID_HOLDS = 12
MAX_HOLDS = 13

__holds = [(0, 17), (0, 15), (0, 14), (0, 13), (0, 12), (0, 11), (0, 10), (0, 9), (0, 8), (0, 4), (1, 17), (1, 15), (1, 14), (1, 12), (1, 11), (1, 10), (1, 9), (1, 8), (1, 7), (1, 6), (1, 5), (1, 3), (1, 2), (2, 17), (2, 15), (2, 14), (2, 13), (2, 12), (2, 11), (2, 10), (2, 9), (2, 8), (2, 7), (2, 6), (2, 5), (2, 4), (3, 2), (3, 17), (3, 16), (3, 15), (3, 14), (3, 13), (3, 12), (3, 11), (3, 10), (3, 9), (3, 8), (3, 7), (3, 6), (3, 5), (3, 4), (4, 17), (4, 15), (4, 14), (4, 13), (4, 12), (4, 11), (4, 10), (4, 9), (4, 8), (4, 7), (4, 6), (4, 5), (5, 15), (5, 14), (5, 13), (5, 12), (5, 11), (5, 10),
            (5, 9), (5, 8), (5, 7), (5, 6), (5, 5), (5, 4), (6, 17), (6, 16), (6, 15), (6, 14), (6, 13), (6, 12), (6, 11), (6, 10), (6, 9), (6, 8), (6, 7), (6, 6), (6, 5), (6, 3), (6, 1), (7, 17), (7, 15), (7, 14), (7, 13), (7, 12), (7, 11), (7, 10), (7, 9), (7, 8), (7, 7), (7, 6), (7, 4), (8, 17), (8, 15), (8, 14), (8, 13), (8, 12), (8, 11), (8, 10), (8, 9), (8, 8), (8, 7), (8, 6), (8, 5), (8, 4), (8, 3), (9, 15), (9, 13), (9, 12), (9, 11), (9, 10), (9, 9), (9, 8), (9, 7), (9, 6), (9, 5), (9, 4), (9, 1), (10, 17), (10, 15), (10, 13), (10, 12), (10, 11), (10, 10), (10, 9), (10, 8), (10, 7), (10, 6), (10, 5), (10, 4)]
ALL_HOLDS = [MoonBoardHold(h[1], h[0]) for h in sorted(__holds, key=lambda x: (x[1], x[0]))]
MIN_START_INDEX = 0
MAX_START_INDEX = util.max_index_with_cond(ALL_HOLDS, lambda h: h.row <= MAX_START_ROW)
MIN_END_INDEX = len(ALL_HOLDS) - COLUMNS + 1
MAX_END_INDEX = len(ALL_HOLDS) - 1
MIN_MID_INDEX = 0
MAX_MID_INDEX = MIN_END_INDEX - 1
START_HOLDS = ALL_HOLDS[MIN_START_INDEX:MAX_START_INDEX+1]
MID_HOLDS = ALL_HOLDS[MIN_MID_INDEX:MAX_MID_INDEX+1]
END_HOLDS = ALL_HOLDS[MIN_END_INDEX:MAX_END_INDEX+1]

HOLE_DISTANCE = 7.875  # square edge size in inches between holds on moonboard
CLIMBER_ARMSPAN = 60
DIST_GRAPH = {hold: {h: util.euclid_distance((hold.col, hold.row), (h.col, h.row)) * HOLE_DISTANCE for h in ALL_HOLDS} for hold in ALL_HOLDS}
REACH_GRAPH = {hold: {h for h in ALL_HOLDS if DIST_GRAPH[hold][h] < CLIMBER_ARMSPAN} for hold in ALL_HOLDS}

HOLD_TYPES = load_hold_types('holdtypes.csv')

def hold_string_range(row: int, start_col: str, end_col: str):
    holds = []
    col = start_col
    while col <= end_col:
        holds.append(col + str(row))
        col = chr(ord(col) + 1)
    return holds


