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
    start = MoonBoardRoute.hold_to_valid_index(route.start_holds[0])
    end = MoonBoardRoute.hold_to_valid_index(route.end_holds[0])
    n_mid = route.num_mid_holds()
    return [start, end, n_mid] + MoonBoardRoute.holds_to_indices(route.mid_holds) + [-1] * (MoonBoardRoute.MAX_MID_HOLDS - n_mid)
    

def ME_params_to_route(in_params: List[int]) -> MoonBoardRoute:
    params = continuous_to_discrete_vals(in_params)
    start = MoonBoardRoute.valid_index_to_hold(params[0])
    end = MoonBoardRoute.valid_index_to_hold(params[1])
    n_mid = params[2]
    mid = MoonBoardRoute.valid_indices_to_holds(params[3: n_mid + 3])
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
