from typing import List, Tuple
from dataclasses import dataclass
import random

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
class MoonboardRoute:
    MOONBOARD_COLUMNS = 11
    MOONBOARD_ROWS = 18

    start_left: int
    start_right: int
    end: int
    holds: List[int]

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
