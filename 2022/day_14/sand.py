import re
from itertools import pairwise, chain

import numpy as np

from utils.aocd_solutions import Puzzle
from utils.grid_2d import coordinates_to_grid, nd_range_inclusive

puzzle = Puzzle(2022, 14)


def walls(data):
    pattern = re.compile(r'(\d+),(\d+)')
    for line in data.split('\n'):
        for p1, p2 in pairwise(tuple(int(g) for g in match.groups()) for match in pattern.finditer(line)):
            yield p1, p2


def create_grid(data):
    coordinates = chain(*(nd_range_inclusive(*wall) for wall in walls(data)))
    return coordinates_to_grid(((coord, 2) for coord in coordinates), start_shape=[1000, 8])


def fill_sand(grid):
    while True:
        tgt = (500, 0)
        if grid[tgt] != 0:
            return
        while True:

            new_tgt = tgt
            for t in [(tgt[0] + x, tgt[1] + 1) for x in [0, -1, 1]]:

                # Check if sand would flow off the bottom of the map
                if t[1] >= grid.shape[1]:
                    return

                if grid[t] == 0:
                    new_tgt = t
                    break

            if new_tgt == tgt:
                grid[tgt] = 1
                break
            tgt = new_tgt


@puzzle.solution_a
def solve_p1(data):
    grid = create_grid(data)
    fill_sand(grid)
    return np.count_nonzero(grid == 1)


@puzzle.solution_b
def solve_p2(data):
    grid = create_grid(data)
    grid = np.pad(grid, ((0, 0), (0, 2)))
    grid[:, -1] = 2
    fill_sand(grid)
    return np.count_nonzero(grid == 1)


puzzle.check_examples()
puzzle.check_solutions()
