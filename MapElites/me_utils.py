from dataclasses import dataclass
import math
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


ROUTE_START_COUNT_I = 0
ROUTE_END_COUNT_I = 3
ROUTE_MID_COUNT_I = 6


def continuous_to_discrete(cont_val: float):
    return math.ceil(cont_val)


def continuous_to_discrete_vals(vals: List[float]):
    return [continuous_to_discrete(v) for v in vals]
    

def route_to_ME_params(route: MoonBoardRoute):
    """
    Format:
    [
        num_start, start_index_1, start_index_2, 
        num_end, end_index_1, end_index_2,
        num_mid, mid_index_1..mid_index_max
    ]
    """
    nstart = route.num_starting_holds()
    nend = route.num_end_holds()
    arr = []
    arr.append(nstart)
    arr += MoonBoardRoute.holds_to_indices(route.start_holds)
    if nstart < 2:
        arr.append(-1)
    arr.append(nend)
    arr += MoonBoardRoute.holds_to_indices(route.end_holds)
    if nend < 2:
        arr.append(-1)
    arr.append(route.num_mid_holds())
    arr += MoonBoardRoute.holds_to_indices(route.mid_holds)
    arr += [-1 for i in range(MoonBoardRoute.MAX_HOLDS - route.num_holds())]
    return arr
    

def ME_params_to_route(params: List[int]) -> MoonBoardRoute:
    si = ROUTE_START_COUNT_I
    ei = ROUTE_END_COUNT_I
    mi = ROUTE_MID_COUNT_I
    n_start = params[si]
    n_end = params[ei]
    n_mid = params[mi]
    start_holds = MoonBoardRoute.valid_indices_to_holds(continuous_to_discrete_vals(params[si + 1: si + n_start + 1]))
    mid_holds = MoonBoardRoute.valid_indices_to_holds(continuous_to_discrete_vals(params[mi + 1: mi + n_mid + 1]))
    end_holds = MoonBoardRoute.valid_indices_to_holds(continuous_to_discrete_vals(params[ei + 1: ei + n_end + 1]))
    return MoonBoardRoute(start_holds=start_holds, mid_holds=mid_holds, end_holds=end_holds)


def get_me_params_bounds():
    max_start_holds = MoonBoardRoute.MAX_START_HOLDS
    max_end_holds = MoonBoardRoute.MAX_END_HOLDS
    start_range = (MoonBoardRoute.min_start_index() - 1, MoonBoardRoute.max_start_index()) # TODO
    end_range = (MoonBoardRoute.min_end_index() - 1, MoonBoardRoute.max_end_index()) # TODO
    mid_range = (-1, len(MoonBoardRoute.index_map_1d()) - 1)
    max_mid_holds = MoonBoardRoute.MAX_HOLDS - (max_start_holds + max_end_holds)

    return [
        (MoonBoardRoute.MIN_START_HOLDS - 1, max_start_holds), # number of start holds
        start_range, # start hold 1 need to figure out max possible index
        start_range, # start hold 2
        (MoonBoardRoute.MIN_END_HOLDS - 1, max_end_holds), # number of end holds
        end_range, # end hold 1 need to figure out index range
        end_range, # end hold 2
        (-1, max_mid_holds)
    ] + [mid_range] * max_mid_holds


    
