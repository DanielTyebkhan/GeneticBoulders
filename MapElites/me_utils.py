from dataclasses import dataclass
import math
from typing import Tuple, List

from share.moonboard_route import MoonBoardRoute
import share.moonboard_util as mu

@dataclass 
class MEParams:
    grid_size: Tuple[int, int]
    bounds: List[Tuple[int, int]]
    batch_size: int
    sigma_0: float
    num_emitters: int
    iterations: int


ROUTE_START_COUNT_I = 0
ROUTE_END_COUNT_I = 3
ROUTE_MID_COUNT_I = 6


def continuous_to_discrete(cont_val: float):
    return math.ceil(cont_val)


def continuous_to_discrete_vals(vals: List[float]):
    return [continuous_to_discrete(v) for v in vals]
    

def route_to_ME_params(route: MoonBoardRoute):
    """
    format: [
        start_hold, end_hold, num_mid, ...mid_holds
    ]
    """
    nmid = route.num_mid_holds()
    return [route.start_holds[0], route.end_holds[0], route.mid_holds] + [None for _ in range(mu.MAX_MID_HOLDS - nmid)]
    

def ME_params_to_route(in_params: List[int]) -> MoonBoardRoute:
    start = in_params[0]
    end = in_params[1]
    mid = [x for x in in_params[2:] if x is not None]
    return MoonBoardRoute(start_holds=[start], end_holds=[end], mid_holds=mid)


def get_me_params_bounds():
    min_mid_holds = mu.MIN_MID_HOLDS
    max_mid_holds = mu.MAX_MID_HOLDS
    start_range = (mu.MIN_START_INDEX - 1, mu.MAX_START_INDEX)
    end_range = (mu.MIN_END_INDEX - 1, mu.MAX_END_INDEX)
    mid_range = (mu.MIN_MID_INDEX - 1, mu.MAX_MID_INDEX)
    num_mid_range = (min_mid_holds - 1, max_mid_holds)
    return [
        start_range,
        end_range,
        num_mid_range,
    ] + [mid_range] * max_mid_holds
