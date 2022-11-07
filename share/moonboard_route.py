import random
from typing import List, Optional

from share.moonboard_util import *
from uuid import UUID, uuid1


class MoonBoardRoute:
    """
    MoonBoard route representation
    Designed for A, B, and Original School hold sets
    """

    def __init__(self, *, start_holds: MoonBoardHolds, mid_holds: MoonBoardHolds, end_holds: MoonBoardHolds, id: Optional[UUID] = None):
        # TODO: deduplicate and copy holds rather than assigning arrays directly
        self.id = id or uuid1()
        self.start_holds = start_holds
        self.mid_holds = mid_holds
        self.end_holds = end_holds

    def get_id_str(self):
        return str(self.id)

    def num_holds(self):
        return self.num_starting_holds() + self.num_mid_holds() + self.num_end_holds()

    def num_starting_holds(self):
        return len(self.start_holds)

    def num_end_holds(self):
        return len(self.end_holds)

    def num_mid_holds(self):
        return len(self.mid_holds)

    def get_all_holds(self) -> MoonBoardHolds:
        return self.start_holds + self.mid_holds + self.end_holds

    def to_strings(self):
        holds = self.get_all_holds()
        return [h.to_coordinate_string() for h in holds]

    def has_feasible_path(self):
        """
        Is there a path through the route in which every move can be spanned?
        """
        def dfs(all_holds: MoonBoardHolds, start, end, path: set):
            if start == end:
                return True
            for h in all_holds:
                if h in REACH_GRAPH[start] and h not in path:
                    path.add(h)
                    if dfs(all_holds, h, end, path):
                        return True
                    path.remove(h)
            return False
        return dfs(self.get_all_holds(), self.start_holds[0], self.end_holds[0], set())

    def is_valid(self):
        """
        Check that the route conforms to restrictions:
            - TODO: if there are two start/end holds, they must be reachable at the same time 
        """
        conditions = [
            MIN_START_HOLDS <= self.num_starting_holds() <= MAX_START_HOLDS,
            MIN_END_HOLDS <= self.num_end_holds() <= MAX_END_HOLDS,
            all([h.row == moonboard_row_to_index(ROWS) for h in self.end_holds]),
            all([h.row <= MAX_START_ROW for h in self.start_holds]),
            all([h in ALL_HOLDS for h in self.get_all_holds()]),
            self.num_holds() <= MAX_HOLDS,
            self.has_feasible_path()
        ]
        return all(conditions)

    ### Static Methods ###

    def get_hold_variety(self):
        # TODO
        return random.randint(1, 5)

    def get_hold_density(self):
        # TODO
        return random.uniform(0, 1)

    def from_hold_strings(*, start_holds: List[str], mid_holds: List[str], end_holds: List[str]):
        start_holds = MoonBoardHold.from_string_list(start_holds)
        mid_holds = MoonBoardHold.from_string_list(mid_holds)
        end_holds = MoonBoardHold.from_string_list(end_holds)
        return MoonBoardRoute(start_holds=start_holds, mid_holds=mid_holds, end_holds=end_holds)

    def make_random():
        # can randomize num start and end holds
        num_start = 1
        num_end = 1
        num_mid = random.randint(MIN_MID_HOLDS, MAX_MID_HOLDS)
        start_holds = random.sample(START_HOLDS, num_start)
        end_holds = random.sample(END_HOLDS, num_end)
        mid_holds = random.sample(MID_HOLDS, num_mid)
        return MoonBoardRoute(start_holds=start_holds, mid_holds=mid_holds, end_holds=end_holds)

    def make_random_valid():
        while not (route := MoonBoardRoute.make_random()).is_valid():
            pass
        return route

    def hold_to_valid_index(hold: MoonBoardHold) -> int:
        return ALL_HOLDS.index(hold)

    def holds_to_indices(holds: MoonBoardHolds) -> List[int]:
        return [MoonBoardRoute.hold_to_valid_index(h) for h in holds]

    def valid_index_to_hold(index: int) -> MoonBoardHold:
        return MoonBoardRoute.ALL_HOLDS[index]

    def valid_indices_to_holds(indices: List[int]) -> MoonBoardHolds:
        return [MoonBoardRoute.valid_index_to_hold(i) for i in indices]
