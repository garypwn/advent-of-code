"""
Tools for manipulating 2-dimensional grid-like structures.

It is assumed that in these structures, indices are in (row, column) order,
and that (0,0) is the top left corner of the structure.
"""
from functools import singledispatch
from typing import Iterable

import numpy as np

UP = (-1, 0)
DOWN = (1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)
DIRECTIONS = {UP, DOWN, LEFT, RIGHT}

CW = {
    UP: RIGHT,
    RIGHT: DOWN,
    DOWN: LEFT,
    LEFT: UP
}

CCW = {
    UP: LEFT,
    RIGHT: UP,
    DOWN: RIGHT,
    LEFT: DOWN
}


@singledispatch
def bounds(arr: np.ndarray or list, idx: tuple[int]) -> bool:
    """Check if a multidimensional array index is in bounds"""
    raise ValueError("Invalid types")


@bounds.register
def _(arr: np.ndarray, idx: tuple[int]):
    return all((0 <= a < b for a, b in zip(idx, arr.shape)))


@bounds.register
def _(arr: list, idx: tuple[int]):
    return all((0 <= a < b for a, b in zip(idx, shape(arr))))


def shape(arr: list) -> tuple:
    """Find the shape of a list of lists. All list lengths must be the same."""
    curr = arr
    s = ()
    while isinstance(curr, list) and len(curr) > 0:
        s += (len(curr),)
        curr = curr[0]

    return s


def chararray(lines: Iterable[str]) -> np.chararray:
    """Transforms lines of text into a 2-dimensional array of single character strings"""
    return np.char.asarray([[s for s in line.strip()] for line in lines], itemsize=1)
