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


ROUTE_START_COUNT_I = 0
ROUTE_END_COUNT_I = 3
ROUTE_MID_COUNT_I = 6


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
    start_holds = MoonBoardRoute.valid_indices_to_holds(params[si + 1: si + n_start + 1])
    mid_holds = MoonBoardRoute.valid_indices_to_holds(params[mi + 1: mi + n_mid + 1])
    end_holds = MoonBoardRoute.valid_indices_to_holds(params[ei + 1: ei + n_end + 1])
    return MoonBoardRoute(start_holds=start_holds, mid_holds=mid_holds, end_holds=end_holds)
