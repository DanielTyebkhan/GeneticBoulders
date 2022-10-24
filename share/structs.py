import random
from typing import List, Optional, Tuple
from dataclasses import dataclass
from uuid import UUID, uuid1

A_OFFSET = 65


@dataclass 
class MEParams:
    grid_size: Tuple[int, int]
    bounds: List[Tuple[int, int]]
    batch_size: int
    sigma_0: float
    num_emitters: int
    iterations: int


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


MoonBoardHolds = List[MoonBoardHold]


@dataclass
class MoonBoardRoute:
    """
    Feet-follow-hands MoonBoard route representation
    Designed for A, B, and Original School hold sets
    """
    COLUMNS = 11
    ROWS = 18
    MAX_START_ROW = 6

    # coordinates not included in the hold sets
    INVALID_HOLDS = [
        'A17', 'B17', 'C17', 'E17', 'F17', 'H17', 'I17', 'J17', 'K17',
        'J15', 'K15', 'B14', 'A8', 'A7', 'A6', 'H6', 'B5', 'E5', 'G5', 
        'A4', 'C4', 'D4', 'F4', 'H4', 'J4', 'K4', 'A3', 'C3', 'K2'
    ] + hold_string_range(3, 'E', 'K') + hold_string_range(2, 'A', 'F') + hold_string_range(2, 'H', 'I') + hold_string_range(1, 'A', 'K')

    mid_holds: MoonBoardHolds
    start_holds: MoonBoardHolds
    end_holds: MoonBoardHolds
    id: UUID

    def __init__(self, start_holds: MoonBoardHolds, mid_holds: MoonBoardHolds, end_holds: MoonBoardHolds, id: Optional[UUID] = None):
        self.id = id or uuid1()
        self.start_holds = start_holds
        self.mid_holds = mid_holds
        self.end_holds = end_holds

        assert self.is_valid()

    def from_hold_strings(start: List[str], mid: List[str], end: List[str]):
        start_holds = MoonBoardHold.from_string_list(start)
        mid_holds = MoonBoardHold.from_string_list(mid)
        end_holds = MoonBoardHold.from_string_list(end)
        return MoonBoardRoute(start_holds, mid_holds, end_holds)

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

    def make_random():
        # can randomize this later
        num_start = 1
        num_end = 1 
        start_holds = []
    
    def is_valid(self):
        """
        Sanity check that the route conforms to items:
        Restrictions:
            - problems all finish on the top row
            - if there are two start/end holds, they must be reachable at the same time
            - all start holds must be on row 6 or lower
            - all holds are actually in the hold set
        """
        conditions = [
            1 <= self.num_starting_holds() <= 2,
            1 <= self.num_end_holds() <= 2,
            all([h.row == moonboard_row_to_index(MoonBoardRoute.ROWS) for h in self.end_holds]),
            all([h.row < MoonBoardRoute.MAX_START_ROW for h in self.start_holds]),
            all([h not in MoonBoardRoute.INVALID_HOLDS for h in self.get_all_holds()])
        ]
        return all(conditions)
