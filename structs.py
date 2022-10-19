from typing import List, Optional, Tuple, TypeAlias
from dataclasses import dataclass
from uuid import UUID, uuid1
import uuid

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


MoonBoardHolds: TypeAlias = List[MoonBoardHold]


@dataclass
class MoonboardRoute:
    MOONBOARD_COLUMNS = 11
    MOONBOARD_ROWS = 18
    INVALID_COORDS = []

    mid_holds: MoonBoardHolds
    start_holds: MoonBoardHolds
    end_hold: MoonBoardHold
    id: UUID

    def __init__(self, start_holds: MoonBoardHolds, mid_holds: MoonBoardHolds, end_hold: MoonBoardHold, id: Optional[UUID] = None):
        self.id = id or uuid1()
        self.start_holds = start_holds
        self.mid_holds = mid_holds
        self.end_hold = end_hold

    def from_hold_strings(start: List[str], mid: List[str], end: str):
        start_holds = MoonBoardHold.from_string_list(start)
        mid_holds = MoonBoardHold.from_string_list(mid)
        end_hold = MoonBoardHold.from_string(end)
        return MoonboardRoute(start_holds, mid_holds, end_hold)

    def get_id_str(self):
        return str(self.id)

    def num_holds(self):
        return len(self.holds)

    def num_starting_holds(self):
        return len(self.start_holds)
