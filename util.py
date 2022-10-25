from typing import List, Callable


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
    