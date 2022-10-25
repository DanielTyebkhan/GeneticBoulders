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


@dataclass
class MoonBoardHold:
    row: int
    col: int

    def from_string(coords: str):
        return MoonBoardHold(row=moonboard_row_to_index(int(coords[1:])), col=moonboard_col_to_index(coords[0]))

    def from_string_list(strlist: List[str]):
        return [MoonBoardHold.from_string(s) for s in strlist]

    def to_coordinate_string(self) -> str:
        return chr(A_OFFSET + self.row) + str(self.col)

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

@dataclass
class MoonBoardRoute:
    """
    Feet-follow-hands MoonBoard route representation
    Designed for A, B, and Original School hold sets
    """
    COLUMNS = 11
    ROWS = 18
    MAX_START_ROW = 5 # 0 based indexing
    
    # TODO: increase maxes to 2
    MIN_START_HOLDS = 1
    MAX_START_HOLDS = 1
    MIN_END_HOLDS = 1
    MAX_END_HOLDS = 1
    MIN_MID_HOLDS = 1
    MAX_MID_HOLDS = 7

    # TODO: double check this restriction
    MAX_HOLDS = 12 # Neural Net Grader can handle at most 12 moves 

    # coordinates not included in the 2016 hold sets
    INVALID_HOLDS = [
        'A17', 'B17', 'C17', 'E17', 'F17', 'H17', 'I17', 'J17', 'K17',
        'J15', 'K15', 'B14', 'A8', 'A7', 'A6', 'H6', 'B5', 'E5', 'G5', 
        'A4', 'C4', 'D4', 'F4', 'H4', 'J4', 'K4', 'A3', 'C3', 'K2'
    ] + hold_string_range(3, 'E', 'K') + hold_string_range(2, 'A', 'F') + hold_string_range(2, 'H', 'I') + hold_string_range(1, 'A', 'K')

    def index_map_1d():
        return [
            h for h in 
                sum([[MoonBoardHold(row, col) for col in range(MoonBoardRoute.COLUMNS)] for row in range(MoonBoardRoute.ROWS)], start=[]) 
            if h not in MoonBoardRoute.INVALID_HOLDS
        ]

    def min_start_index():
        return 0

    def max_start_index():
        return util.max_index_with_cond(MoonBoardRoute.index_map_1d(), lambda h: h.row <= MoonBoardRoute.MAX_START_ROW)

    def min_end_index():
        return util.min_index_with_cond(MoonBoardRoute.index_map_1d(), lambda h: h.row == MoonBoardRoute.ROWS - 1)

    def max_end_index():
        return len(MoonBoardRoute.index_map_1d()) - 1


    mid_holds: MoonBoardHolds
    start_holds: MoonBoardHolds
    end_holds: MoonBoardHolds
    id: UUID

    def __init__(self, *, start_holds: MoonBoardHolds, mid_holds: MoonBoardHolds, end_holds: MoonBoardHolds, id: Optional[UUID] = None):
        # TODO: deduplicate and copy holds rather than assigning arrays directly
        self.id = id or uuid1()
        self.start_holds = start_holds
        self.mid_holds = mid_holds
        self.end_holds = end_holds

    def from_hold_strings(*, start_holds: List[str], mid_holds: List[str], end_holds: List[str]):
        start_holds = MoonBoardHold.from_string_list(start_holds)
        mid_holds = MoonBoardHold.from_string_list(mid_holds)
        end_holds = MoonBoardHold.from_string_list(end_holds)
        return MoonBoardRoute(start_holds=start_holds, mid_holds=mid_holds, end_holds=end_holds)

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

    def make_random():
        # can randomize num start and end holds
        num_start = 1
        num_end = 1 
        num_mid = random.randint(MoonBoardRoute.MIN_MID_HOLDS, MoonBoardRoute.MAX_MID_HOLDS)
        start_holds = [MoonBoardHold.make_random_start() for _ in range(num_start)]
        end_holds = [MoonBoardHold.make_random_end() for _ in range(num_end)]
        mid_holds = [MoonBoardHold.make_random() for _ in range(num_mid)]
        return MoonBoardRoute(start_holds=start_holds, mid_holds=mid_holds, end_holds=end_holds)

    def make_random_valid():
        while not (route := MoonBoardRoute.make_random()).is_valid():
            pass
        return route

    def rand_col():
        return random.randint(0, MoonBoardRoute.COLUMNS - 1)

    def rand_row():
        return random.randint(0, moonboard_row_to_index(MoonBoardRoute.ROWS))

    def rand_start_row():
        return random.randint(0, MoonBoardRoute.MAX_START_ROW)
    
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
            MoonBoardRoute.MIN_START_HOLDS <= self.num_starting_holds() <= MoonBoardRoute.MAX_START_HOLDS,
            MoonBoardRoute.MIN_END_HOLDS <= self.num_end_holds() <= MoonBoardRoute.MAX_END_HOLDS,
            all([h.row == moonboard_row_to_index(MoonBoardRoute.ROWS) for h in self.end_holds]),
            all([h.row <= MoonBoardRoute.MAX_START_ROW for h in self.start_holds]),
            all([h not in MoonBoardRoute.INVALID_HOLDS for h in self.get_all_holds()]),
            self.num_holds() <= MoonBoardRoute.MAX_HOLDS
        ]
        return all(conditions)

    def get_hold_variety(self):
        # TODO
        return random.randint(1, 5)
    
    def get_hold_density(self):
        # TODO
        return random.uniform(0, 1)

    def hold_to_valid_index(hold: MoonBoardHold) -> int:
        return MoonBoardRoute.index_map_1d().index(hold)

    def holds_to_indices(holds: MoonBoardHolds) -> List[int]:
        return [MoonBoardRoute.hold_to_valid_index(h) for h in holds]

    def valid_index_to_hold(index: int) -> MoonBoardHold:
        return MoonBoardRoute.index_map_1d()[index]

    def valid_indices_to_holds(indices: List[int]) -> MoonBoardHolds:
        return [MoonBoardRoute.valid_index_to_hold(i) for i in indices]

