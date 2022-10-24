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
    