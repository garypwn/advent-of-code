import re
from itertools import product

import numpy as np

from utils.aocd_solutions import Puzzle
from utils.grid_2d import chararray

puzzle = Puzzle(2024, 4)


def count_words(array, pattern: re.Pattern):
    ct = 0
    for line in array:
        for _ in pattern.finditer(''.join(line)):
            ct += 1
    for line in diagonalize(array):
        for _ in pattern.finditer(''.join(line)):
            ct += 1
    return ct


def diagonalize(array):
    def diagonal_iter(h, w):
        for i in range(h):
            yield zip(range(i, -1, -1), range(0, min(i + 1, w)))
        for i in range(1, w):
            yield zip(range(h - 1, -1, -1), range(i, w))

    for indices in diagonal_iter(len(array), len(array[0])):
        yield ''.join([array[idx] for idx in indices])


@puzzle.solution_a
def solve_p1(data):
    grid = chararray(data.split('\n'))
    ct = 0
    pattern = re.compile(r"XMAS")
    for view in [np.rot90(grid, x) for x in [0, 1, 2, 3]]:
        ct += count_words(view, pattern)
    return ct


@puzzle.solution_b
def solve_p2(data):
    grid = chararray(data.split('\n'))
    ct = 0
    for i, j in product(*[range(x) for x in grid.shape]):
        mas = 0
        for view in [np.rot90(grid[i:i + 3, j:j + 3], x) for x in range(4)]:
            if "MAS" in diagonalize(view):
                mas += 1
        if mas >= 2:
            ct += 1

    return ct


puzzle.check_examples()
puzzle.check_solutions()
