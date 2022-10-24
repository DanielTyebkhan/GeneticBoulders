from dataclasses import dataclass
from typing import Tuple, List

from share.moonboard_util import MoonBoardRoute

@dataclass 
class MEParams:
    grid_size: Tuple[int, int]
    bounds: List[Tuple[int, int]]
    batch_size: int
    sigma_0: float
    num_emitters: int
    iterations: int


def route_to_ME_params(route: MoonBoardRoute):
    

