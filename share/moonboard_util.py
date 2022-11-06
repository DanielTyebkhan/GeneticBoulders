from collections import defaultdict
from math import sqrt
import random
from typing import List, Optional, Tuple
from dataclasses import dataclass
from uuid import UUID, uuid1
from share import valid_holds
import util

A_OFFSET = 65


def moonboard_row_to_index(row: int) -> int:
    return row - 1


def moonboard_col_to_index(col: str) -> int:
    return ord(col) - A_OFFSET


def hold_string_range(row: int, start_col: str, end_col: str):
    holds = []
    col = start_col
    while col <= end_col:
        holds.append(col + str(row))
        col = chr(ord(col) + 1)
    return holds


@dataclass(frozen=True)
class MoonBoardHold:
    row: int
    col: int

    def from_string(coords: str):
        return MoonBoardHold(row=moonboard_row_to_index(int(coords[1:])), col=moonboard_col_to_index(coords[0]))

    def from_string_list(strlist: List[str]):
        return [MoonBoardHold.from_string(s) for s in strlist]

    def to_coordinate_string(self) -> str:
        return chr(A_OFFSET + self.col) + str(self.row + 1)

    def is_valid(self) -> bool:
        return (self.col, self.row) in valid_holds.ALL_HOLDS

    def from_xy(x, y):
        return MoonBoardHold(row=y, col=x)

    def __rand_from_list(ls):
        x, y = random.choice(ls)
        return MoonBoardHold.from_xy(x, y)

    def make_random():
        return MoonBoardHold.__rand_from_list(valid_holds.ALL_HOLDS)

    def make_random_start():
        return MoonBoardHold.__rand_from_list(valid_holds.START_HOLDS)

    def make_random_end():
        return MoonBoardHold.__rand_from_list(valid_holds.END_HOLDS)


MoonBoardHolds = List[MoonBoardHold]

class MoonBoardRoute:
    """
    Feet-follow-hands MoonBoard route representation
    Designed for A, B, and Original School hold sets
    """
    COLUMNS = 11
    ROWS = 18
    MAX_START_ROW = 5  # 0 based indexing

    # TODO: increase maxes to 2
    MIN_START_HOLDS = 1
    MAX_START_HOLDS = 1
    MIN_END_HOLDS = 1
    MAX_END_HOLDS = 1
    MIN_MID_HOLDS = 4
    MAX_MID_HOLDS = 7
    MAX_HOLDS = 12

    # unordered list of all valid holds in setup
    __holds = [(0, 17), (0, 15), (0, 14), (0, 13), (0, 12), (0, 11), (0, 10), (0, 9), (0, 8), (0, 4), (1, 17), (1, 15), (1, 14), (1, 12), (1, 11), (1, 10), (1, 9), (1, 8), (1, 7), (1, 6), (1, 5), (1, 3), (1, 2), (2, 17), (2, 15), (2, 14), (2, 13), (2, 12), (2, 11), (2, 10), (2, 9), (2, 8), (2, 7), (2, 6), (2, 5), (2, 4), (3, 2), (3, 17), (3, 16), (3, 15), (3, 14), (3, 13), (3, 12), (3, 11), (3, 10), (3, 9), (3, 8), (3, 7), (3, 6), (3, 5), (3, 4), (4, 17), (4, 15), (4, 14), (4, 13), (4, 12), (4, 11), (4, 10), (4, 9), (4, 8), (4, 7), (4, 6), (4, 5), (5, 17), (5, 15), (5, 14), (5, 13), (5, 12), (5, 11), (5, 10),
                (5, 9), (5, 8), (5, 7), (5, 6), (5, 5), (5, 4), (6, 17), (6, 16), (6, 15), (6, 14), (6, 13), (6, 12), (6, 11), (6, 10), (6, 9), (6, 8), (6, 7), (6, 6), (6, 5), (6, 3), (6, 1), (7, 17), (7, 15), (7, 14), (7, 13), (7, 12), (7, 11), (7, 10), (7, 9), (7, 8), (7, 7), (7, 6), (7, 4), (8, 17), (8, 15), (8, 14), (8, 13), (8, 12), (8, 11), (8, 10), (8, 9), (8, 8), (8, 7), (8, 6), (8, 5), (8, 4), (8, 3), (9, 15), (9, 13), (9, 12), (9, 11), (9, 10), (9, 9), (9, 8), (9, 7), (9, 6), (9, 5), (9, 4), (9, 1), (10, 17), (10, 15), (10, 13), (10, 12), (10, 11), (10, 10), (10, 9), (10, 8), (10, 7), (10, 6), (10, 5), (10, 4)]
    ALL_HOLDS = [MoonBoardHold(h[1], h[0]) for h in sorted(__holds, lambda x: (x[0], x[1]))]
    MIN_START_INDEX = 0
    MAX_START_INDEX = util.max_index_with_cond(ALL_HOLDS, lambda h: h.row <= MoonBoardRoute.MAX_START_ROW)
    MIN_END_INDEX = len(ALL_HOLDS) - COLUMNS + 1
    MAX_END_INDEX = len(ALL_HOLDS) - 1
    MIN_MID_INDEX = 0
    MAX_MID_INDEX = MIN_END_INDEX - 1
    START_HOLDS = ALL_HOLDS[MIN_START_INDEX:MAX_START_INDEX]
    END_HOLDS = ALL_HOLDS[MIN_END_INDEX:MAX_END_INDEX]

    HOLE_DISTANCE = 7.875  # square edge size in inches between holds on moonboard
    CLIMBER_ARMSPAN = 69
    REACH_GRAPH = {
        hold: {h for h in MoonBoardRoute.ALL_HOLDS if util.euclid_distance(hold, h) < MoonBoardRoute.CLIMBER_ARMSPAN} for hold in ALL_HOLDS
    }

    def __init__(self, *, start_holds: MoonBoardHolds, mid_holds: MoonBoardHolds, end_holds: MoonBoardHolds, id: Optional[UUID] = None):
        # TODO: deduplicate and copy holds rather than assigning arrays directly
        self.id = id or uuid1()
        self.start_holds = start_holds
        self.mid_holds = mid_holds
        self.end_holds = end_holds

    def get_id_str(self):
        return str(self.id)

    def num_holds(self):
        return self.num_starting_holds() + self.num_mid_holds() + self.num_end_holds()

    def num_starting_holds(self):
        return len(self.start_holds)

    def num_end_holds(self):
        return len(self.end_holds)

    def num_mid_holds(self):
        return len(self.mid_holds)

    def get_all_holds(self) -> MoonBoardHolds:
        return self.start_holds + self.mid_holds + self.end_holds

    def to_strings(self):
        holds = self.get_all_holds()
        return [h.to_coordinate_string() for h in holds]

    def has_feasible_path(self):
        """
        Is there a path through the route in which every move can be spanned?
        """
        def dfs(all_holds: MoonBoardHolds, start, end, path: set):
            if start == end:
                return True
            for h in all_holds:
                if h in MoonBoardRoute.REACH_GRAPH[start] and h not in path:
                    path.add(h)
                    if dfs(all_holds, h, end, path):
                        return True
                    path.remove(h)
            return False
        
        return dfs(self.get_all_holds(), self.start_holds[0], self.end_holds[0], set())
                    

        return True

    def is_valid(self):
        """
        Check that the route conforms to restrictions:
            - problems finish on the top row
            - all start holds must be on row 6 or lower
            - all holds are actually in the hold set
            - there are no more than the max number of holds
            - TODO: if there are two start/end holds, they must be reachable at the same time 
            - TODO: lowest start hold should be lowest hold
        """
        conditions = [
            MoonBoardRoute.MIN_START_HOLDS <= self.num_starting_holds(
            ) <= MoonBoardRoute.MAX_START_HOLDS,
            MoonBoardRoute.MIN_END_HOLDS <= self.num_end_holds() <= MoonBoardRoute.MAX_END_HOLDS,
            all([h.row == moonboard_row_to_index(MoonBoardRoute.ROWS)
                for h in self.end_holds]),
            all([h.row <= MoonBoardRoute.MAX_START_ROW for h in self.start_holds]),
            all([h not in MoonBoardRoute.INVALID_HOLDS for h in self.get_all_holds()]),
            self.num_holds() <= MoonBoardRoute.MAX_HOLDS,
            self.has_feasible_path()
        ]
        return all(conditions)

    ### Static Methods ###

    def get_hold_variety(self):
        # TODO
        return random.randint(1, 5)

    def get_hold_density(self):
        # TODO
        return random.uniform(0, 1)

    def from_hold_strings(*, start_holds: List[str], mid_holds: List[str], end_holds: List[str]):
        start_holds = MoonBoardHold.from_string_list(start_holds)
        mid_holds = MoonBoardHold.from_string_list(mid_holds)
        end_holds = MoonBoardHold.from_string_list(end_holds)
        return MoonBoardRoute(start_holds=start_holds, mid_holds=mid_holds, end_holds=end_holds)

    def make_random():
        # can randomize num start and end holds
        num_start = 1
        num_end = 1
        num_mid = random.randint(
            MoonBoardRoute.MIN_MID_HOLDS, MoonBoardRoute.MAX_MID_HOLDS)
        start_holds = [MoonBoardHold.make_random_start()
                       for _ in range(num_start)]
        end_holds = [MoonBoardHold.make_random_end() for _ in range(num_end)]
        mid_holds = [MoonBoardHold.make_random() for _ in range(num_mid)]
        return MoonBoardRoute(start_holds=start_holds, mid_holds=mid_holds, end_holds=end_holds)

    def make_random_valid():
        while not (route := MoonBoardRoute.make_random()).is_valid():
            pass
        return route

    def hold_to_valid_index(hold: MoonBoardHold) -> int:
        return MoonBoardRoute.ALL_HOLDS.index(hold)

    def holds_to_indices(holds: MoonBoardHolds) -> List[int]:
        return [MoonBoardRoute.hold_to_valid_index(h) for h in holds]

    def valid_index_to_hold(index: int) -> MoonBoardHold:
        return MoonBoardRoute.ALL_HOLDS[index]

    def valid_indices_to_holds(indices: List[int]) -> MoonBoardHolds:
        return [MoonBoardRoute.valid_index_to_hold(i) for i in indices]
