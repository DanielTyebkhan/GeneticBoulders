import pickle
import math
from typing import Iterable, List, Callable

A_OFFSET = 65

def euclid_distance(p1: Iterable, p2: Iterable):
    return math.sqrt(sum([(c1 - c2)**2 for c1, c2 in zip(p1, p2)]))


def max_index_with_cond(ls: List, cond: Callable[[any], bool]) -> int:
    """
    ls must have at least one element matching cond
    """
    index = -1
    while cond(ls[index + 1]):
        index += 1
    return index


def min_index_with_cond(ls: List, cond: Callable[[any], bool]) -> int:
    """
    ls must have at least one element matching cond
    """
    index = 0
    while not cond(ls[index]):
        index += 1
    return index
    

def save_pickle(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)


def load_pickle(path):
    with open(path, 'rb') as f:
        obj = pickle.load(f)
    return obj