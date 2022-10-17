from typing import List, Tuple
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


@dataclass
class Coordinate:
    x: int
    y: int

@dataclass
class MoonBoardRouteHold:
    row: int
    col: int
    is_start: bool
    is_end: bool

    def from_string(coords: str, is_start=False, is_end=False):
        return MoonBoardRouteHold(row=int(coords[1:]) - 1, col=ord(coords[0]) - A_OFFSET, is_start=is_start, is_end=is_end)

    def get_coordinate_string(self):
        return chr(A_OFFSET + self.row) + str(self.col)

    def to_dict(self):
        return {
            'Description': self.col + str(self.row), 
            'IsStart': self.is_start,
            'IsEnd': self.is_end
        }


@dataclass
class MoonboardRoute:
    MOONBOARD_COLUMNS = 11
    MOONBOARD_ROWS = 18
    INVALID_COORDS = []

    holds: List[MoonBoardRouteHold]
    id: UUID

    def __init__(self, holds: List[MoonBoardRouteHold]):
        self.id = uuid1()
        self.holds = holds

    def from_hold_strings(holds: List[str], start: List[str], end: str):
        all_holds = [MoonBoardRouteHold.from_string(h) for h in holds]
        all_holds.extend([MoonBoardRouteHold.from_string(h, is_start=True) for h in start])
        all_holds.append(MoonBoardRouteHold.from_string(end, is_end=True))
        return MoonboardRoute(all_holds)

    def get_id_str(self):
        return str(self.id)

    '''
    ls should be of form
        [start, end, ...holds]
    where start
    '''
    def from_list(ls: List):
        return MoonboardRoute(start_left=ls[0], start_right=ls[1], end=ls[2], holds=ls[3:])

    def num_holds(self):
        return len(self.holds)

    def num_starting_holds(self):
        return len(self.starting_holds())

    def num_ending_holds(self):
        return len(self.ending_holds())

    def starting_holds(self):
        return [h for h in self.holds if h.is_start]

    def ending_holds(self):
        return [h for h in self.holds if h.is_end]

