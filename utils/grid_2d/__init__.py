"""
Tools for manipulating 2-dimensional grid-like structures.

It is assumed that in these structures, indices are in (row, column) order,
and that (0,0) is the top left corner of the structure.
"""
from collections.abc import Iterable
from functools import singledispatch

import numpy as np
import numpy.typing as npt

from utils.vector import Vector2

UP = (-1, 0)
DOWN = (1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)

UP_RIGHT = (-1, 1)
UP_LEFT = (-1, -1)
DOWN_RIGHT = (1, 1)
DOWN_LEFT = (1, -1)

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
DIRECTIONS_V = [Vector2(d) for d in DIRECTIONS]
DIRECTIONS_DIAG = [UP_RIGHT, UP_LEFT, DOWN_RIGHT, DOWN_LEFT]
DIRECTIONS_NP = [np.asarray(d) for d in DIRECTIONS]

CW = {
    UP: RIGHT,
    RIGHT: DOWN,
    DOWN: LEFT,
    LEFT: UP,

    UP_RIGHT: DOWN_RIGHT,
    DOWN_RIGHT: DOWN_LEFT,
    DOWN_LEFT: UP_LEFT,
    UP_LEFT: UP_RIGHT
}

CCW = {
    UP: LEFT,
    RIGHT: UP,
    DOWN: RIGHT,
    LEFT: DOWN,

    UP_RIGHT: UP_LEFT,
    DOWN_RIGHT: UP_RIGHT,
    DOWN_LEFT: DOWN_RIGHT,
    UP_LEFT: DOWN_LEFT
}

DIRECTION_DICT = {
    'U': UP, 'D': DOWN, 'L': LEFT, 'R': RIGHT,
    'N': UP, 'S': DOWN, 'W': LEFT, 'E': RIGHT,
    '^': UP, 'v': DOWN, '<': LEFT, '>': RIGHT,
    'NE': UP_RIGHT, 'NW': UP_LEFT, 'SE': DOWN_RIGHT, 'SW': DOWN_LEFT
}


@singledispatch
def bounds() -> bool:
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


def chararray(lines: Iterable[str]) -> np.char.chararray:
    """Transforms lines of text into a 2-dimensional array of single character strings"""
    return np.char.asarray([[s for s in line.strip()] for line in lines], itemsize=1)


def coordinates_to_grid(values: Iterable[tuple[npt.ArrayLike, int]], start_shape=(20, 20), fill=0) -> np.ndarray:
    """Creates a grid from a list of ((x,y), val) coordinate-value pairs"""
    grid = np.full(start_shape, fill)
    for pt, value in values:
        if any(a >= b for a, b in zip(pt, grid.shape)):
            pad = np.asarray([(0, max(0, a - b + 1)) for a, b in zip(pt, grid.shape)])
            grid = np.pad(array=grid, pad_width=pad, constant_values=0)

        grid[pt] = value

    return grid


def grid_to_coordinates(arr: Iterable[Iterable], ignore=None):
    """Given a 2d grid, creates a dict of {val: [pts]} that maps unique tokens to lists of points where they occur.
    Specifying a list of tokens to ignore can be helpful for ignoring 'background' tokens."""
    pts = dict()
    for i, line in enumerate(arr):
        for j, c in enumerate(line):
            if ignore is not None and c in ignore:
                continue
            if c in pts:
                pts[c].add(Vector2(i, j))
            else:
                pts[c] = {Vector2(i, j)}
    return pts


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


def diag_range(stop_1, stop_2):
    """Yields lists of indices representing diagonal rows in a grid."""
    for i in range(stop_1):
        yield zip(range(i, -1, -1), range(0, min(i + 1, stop_2)))
    for i in range(1, stop_2):
        yield zip(range(stop_1 - 1, -1, -1), range(i, stop_2))


def diag_iter(arr):
    """Yields diagonal rows of a grid"""
    for row in diag_range(len(arr), len(arr[0])):
        yield (arr[i][j] for i, j in row)


def diag_enumerate(arr):
    """Yields diagonal rows of a grid with indices"""
    for row in diag_range(len(arr), len(arr[0])):
        yield (((i, j), arr[i][j]) for i, j in row)
