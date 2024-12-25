from itertools import product

import numpy as np

from utils.aocd_solutions import Puzzle
from utils.grid_2d import chararray

puzzle = Puzzle(2024, 25)


def parse(data):
    keys, locks = [], []
    for block in data.split('\n\n'):
        block = chararray(block.split('\n'))
        if key := np.all(block[0] == '.'):
            block = np.flip(block, 0)
        heights = [np.flatnonzero(col == '#')[-1] for col in block.transpose()]
        if key:
            keys.append(heights)
        else:
            locks.append(heights)
    return keys, locks


@puzzle.solution_a
def solve_p1(data):
    ct = 0
    for key, lock in product(*parse(data)):
        heights = [k + l for k, l in zip(key, lock)]
        if all(h < 6 for h in heights):
            ct += 1
    return ct


puzzle.check_solutions()
