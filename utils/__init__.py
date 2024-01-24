from functools import cache

import numpy as np

UP = (-1, 0)
DOWN = (1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)
DIRECTIONS = {UP, DOWN, LEFT, RIGHT}


@cache
def add(t1: tuple, t2: tuple) -> tuple:
    return tuple(a + b for a, b in zip(t1, t2))


@cache
def sub(t1: tuple, t2: tuple) -> tuple:
    return tuple(a - b for a, b in zip(t1, t2))


@cache
def neg(t: tuple) -> tuple:
    return tuple(-a for a in t)


def bounds(pt: tuple, arr: np.array) -> bool:
    return all((0 <= a < b for a, b in zip(pt, arr.shape)))
