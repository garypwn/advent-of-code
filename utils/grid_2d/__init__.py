"""
Tools for manipulating 2-dimensional grid-like structures.

It is assumed that in these structures, indices are in (row, column) order,
and that (0,0) is the top left corner of the structure.
"""
from collections.abc import Iterable
from functools import singledispatch
from itertools import chain

import numpy as np
import numpy.typing as npt

UP = (-1, 0)
DOWN = (1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)
DIRECTIONS = {UP, DOWN, LEFT, RIGHT}
DIRECTIONS_NP = [np.asarray(d) for d in DIRECTIONS]

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

DIRECTION_DICT = {
    'U': UP, 'D': DOWN, 'L': LEFT, 'R': RIGHT
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


def coordinates_to_grid(values: Iterable[tuple[npt.ArrayLike, int]], start_shape=(20, 20), fill=0) -> np.ndarray:
    grid = np.full(start_shape, fill)
    for pt, value in values:
        if any(a >= b for a, b in zip(pt, grid.shape)):
            pad = [(0, max(0, a - b + 1)) for a, b in zip(pt, grid.shape)]
            grid = np.pad(grid, pad, constant_values=fill)

        grid[pt] = value

    return grid


def nd_range_inclusive(c1: npt.ArrayLike | None, c2=npt.ArrayLike | None):
    """
    Generates an inclusive n-dimensional range of tuples based on two input ranges.
    Both c1 and c2 are included in the output.
    Useful for making rectangles out of two points.
    """
    if not c1 and not c2:
        return None

    start = min(c1[0] if c1 else 0, c2[0] if c2 else 0)
    stop = max(c1[0] if c1 else 0, c2[0] if c2 else 0)

    if len(c1) == 1:
        for i in range(start, stop + 1):
            yield (i,)
    else:
        for i in range(start, stop + 1):
            for j in nd_range_inclusive(c1[1:] if c1 else None, c2[1:] if c2 else None):
                yield (i,) + j
