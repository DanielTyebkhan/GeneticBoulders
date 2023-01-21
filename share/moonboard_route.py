import random
from typing import List, Optional

import numpy as np

from share.moonboard_util import *
from uuid import UUID, uuid1
import MoonBoardRNN.BetaMove.preprocessing_helper as ph
from MoonBoardRNN.BetaMove.BetaMove import load_feature_dict


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
        self.beta = None

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
        def dfs(all_holds: set, start, end, seen):
            if start == end:
                return True
            if start not in seen:
                seen.add(start)
                for h in all_holds.intersection(REACH_GRAPH[start]):
                    if (dfs(all_holds, h, end)):
                        return True
            return False
        return dfs(set(self.get_all_holds()), self.start_holds[0], self.end_holds[0], set())

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
            # self.has_feasible_path()
        ]
        valid = all(conditions)
        return valid

    def get_hold_variety(self):
        return len({HOLD_TYPES[h] for h in self.get_all_holds()})

    def get_max_span(self, feature_dict=None):
        beta = self.get_beta(feature_dict)
        coords = [MoonBoardHold.from_beta_vector(v) for v in beta.allHolds]
        joined = zip(beta.handOperator, beta.handSequence)
        left = next(joined)[1]
        right = next(joined)[1]
        while True:
            max_span = DIST_GRAPH[coords[left]][coords[right]]
            hand, index = next(joined, (None, None))
            if hand is None:
                break
            if hand[0] == 'L':
                left = index
            else:
                right = index
        return max_span / 12

    def classify_and_reorganize_data_ga(self, feature_dict=None):
        if feature_dict is None:
            feature_dict = load_feature_dict()

        n_start = self.num_starting_holds()
        n_mid = self.num_mid_holds()
        n_hold = self.num_holds()
        start_sorted = sorted(self.start_holds, key=lambda h: h.row)
        mid_sorted = sorted(self.mid_holds, key=lambda h: h.row)
        end_sorted = sorted(self.end_holds, key=lambda h: h.row)
        all_holds = start_sorted + mid_sorted + end_sorted

        x_vectors = np.zeros((10, n_hold))
        for i, hold in enumerate(all_holds):
            x, y = hold.col, hold.row
            x_vectors[0:6, i] = feature_dict[(x, y)] # hand feature encoding
            x_vectors[6:8, i] = [x, y] # coordinate encoding
        x_vectors[8:, 0:n_start] = np.array([[1], [0]])
        x_vectors[8:, n_start + n_mid:] = np.array([[0], [1]])
        return x_vectors

    def to_x_vectors(self, feature_dict=None):
        beta = self.get_beta(feature_dict)
        x_vectors = beta.to_x_vectors()
        return x_vectors

    def purge_holds(self, feature_dict=None):
        beta = self.get_beta(feature_dict)
        unused = beta.holdsNotUsed
        for index in unused:
            vec = beta.getAllHolds()[index]
            hold = MoonBoardHold.from_beta_vector(vec)
            if hold in self.start_holds:
                self.start_holds.remove(hold)
            if hold in self.mid_holds:
                self.mid_holds.remove(hold)
            if hold in self.start_holds:
                self.end_holds.remove(hold)

    def get_beta(self, feature_dict=None) -> ph.beta:
        if self.beta is None:
            route_id = self.get_id_str()
            data_dict = {route_id: self.classify_and_reorganize_data_ga(feature_dict=feature_dict)}
            self.beta = ph.produce_sequence(route_id, data_dict, printout=False)[0]
        return self.beta


    ### Static Methods ###

    def from_hold_strings(*, start_holds: List[str], mid_holds: List[str], end_holds: List[str]):
        start_holds = MoonBoardHold.from_string_list(start_holds)
        mid_holds = MoonBoardHold.from_string_list(mid_holds)
        end_holds = MoonBoardHold.from_string_list(end_holds)
        return MoonBoardRoute(start_holds=start_holds, mid_holds=mid_holds, end_holds=end_holds)

    def make_random():
        # can randomize num start and end holds in future
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
        return ALL_HOLDS[index]

    def valid_indices_to_holds(indices: List[int]) -> MoonBoardHolds:
        return [MoonBoardRoute.valid_index_to_hold(i) for i in indices]
