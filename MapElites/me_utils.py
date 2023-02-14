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
    num_emitters: int
    iterations: int


def continuous_to_discrete(cont_val: float) -> int:
    return math.ceil(cont_val)


def grade_string_to_num(grade: str) -> int:
    return int(grade[1:])


def continuous_to_discrete_vals(vals: List[float]) -> List[int]:
    return [continuous_to_discrete(v) for v in vals]
    

def route_to_ME_params(route: MoonBoardRoute) -> List[int]:
    """
    Returns a 13 element array of hold indices.
    A value of -1 indicates no hold
    """
    nmid = route.num_mid_holds()
    arr = [route.start_holds[0], route.end_holds[0]] + route.mid_holds
    return [MoonBoardRoute.hold_to_valid_index(h) for h in arr] + ([-1] * (mu.MAX_MID_HOLDS - nmid))
    

def ME_params_to_route(in_params: List[int]) -> MoonBoardRoute:
    holds = [MoonBoardRoute.valid_index_to_hold(x) for x in in_params if x != -1]
    start = holds[0]
    end = holds[1]
    mid = holds[2:]
    return MoonBoardRoute(start_holds=[start], end_holds=[end], mid_holds=mid)


def get_me_params_bounds() -> List[float]:
    """
    Deprecated param bounds from float representation of MoonBoard Elites
    """
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

def grade_diff_from_fitness(fit):
    if fit == 0:
        return 10
    return int(1 / fit)
