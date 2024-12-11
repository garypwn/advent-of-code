import numpy as np

from utils import tuples
from utils.aocd_solutions import Puzzle
from utils.grid_2d import DIRECTIONS

puzzle = Puzzle(2024, 10)


def parse(data):
    return np.asarray([[int(s) for s in line.strip()] for line in data.split('\n')])

def spanning(pt, grid):
    for d in DIRECTIONS:
        tgt = tuples.add(pt, d)
        if all(0 <= u < s for u, s in zip(tgt, grid.shape)) and grid[pt] == grid[tgt] + 1:
            val = grid[tgt]
            yield tgt, val
            for t in spanning(tgt, grid):
                yield t

def count_trails(pt, grid):
    for d in DIRECTIONS:
        tgt = tuples.add(pt, d)
        if all(0 <= u < s for u, s in zip(tgt, grid.shape)) and grid[pt] + 1 == grid[tgt]:
            val = grid[tgt]
            if val == 9:
                yield tgt
            for t in count_trails(tgt, grid):
                yield t

@puzzle.solution_a
def solve_p1(data):
    grid = parse(data)
    spans = {pt: set(spanning(pt, grid)) for pt in zip(*np.where(grid == 9))}
    return sum(len([pt for pt, val in span if val == 0]) for span in spans.values())

@puzzle.solution_b
def solve_p2(data):
    grid = parse(data)
    return sum(len([None for _ in count_trails(pt, grid)]) for pt in zip(*np.where(grid == 0)))

puzzle.check_solutions()
