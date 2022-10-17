from typing import List, Tuple
from dataclasses import dataclass
import random
from uuid import UUID, uuid1

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

class MoonBoardRouteHold:
    row: int
    col: str
    is_start: bool
    is_end: bool

    def from_string(coords: str, is_start=False, is_end=False):
        return MoonBoardRouteHold(row=int(coords[1:]), col=coords[0], is_start=is_start, is_end=is_end)

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

    def to_dict(self):
        return {'moves': self.holds}

    '''
    ls should be of form
        [start, end, ...holds]
    where start
    '''
    def from_list(ls: List):
        return MoonboardRoute(start_left=ls[0], start_right=ls[1], end=ls[2], holds=ls[3:])

    def __rand_column():
        return random.randint(0, MoonboardRoute.MOONBOARD_COLUMNS)

    def randomize():
        return MoonboardRoute(
            start_left=MoonboardRoute.__rand_column(), 
            start_right=MoonboardRoute.__rand_column(),
            end=MoonboardRoute.__rand_column()
            holds=[random.randint(0,1) for _ in range(MoonboardRoute.MOONBOARD_COLUMNS * MoonboardRoute.MOONBOARD_ROWS)])
