import sys
from copy import copy
from itertools import product

import numpy as np

from utils import tuples
from utils.aocd_solutions import Puzzle
from utils.grid_2d import DIRECTIONS, CCW, CW

puzzle = Puzzle(2024, 12)


def parse_grid(data):
    return np.asarray([[ord(s) for s in line] for line in data.split('\n')], dtype=int)


def get_regions(grid):
    accounted = set()

    for start in product(*(range(s) for s in grid.shape)):
        if start in accounted:
            continue

        # Simple BFS from each unaccounted pt
        val = grid[start]
        zone = set()  # Set of pts in the region
        perimeter = set()  # Set of (pt, tgt) pairs that make up the perimeter
        q = {start}
        while q:
            pt = q.pop()
            zone.add(pt)

            for d in DIRECTIONS:
                tgt = tuples.add(d, pt)
                if tgt not in zone:
                    if all((0 <= p < s for p, s in zip(tgt, grid.shape))) and grid[tgt] == val:
                        q.add(tgt)
                    else:
                        perimeter.add((pt, tgt))

            accounted.add(pt)

        yield zone, perimeter


def count_sides(edges):
    sides = 0
    # edges = copy(edges)  # Don't destroy edges
    while edges:
        e = edges.pop()
        edge_d = tuples.sub(*e)

        # Here we're just going along the side and popping entries from edges
        for d in (CCW[edge_d], CW[edge_d]):
            for i in range(1, sys.maxsize):
                e2 = tuple(tuples.add(pt, tuples.scale(d, i)) for pt in e)
                if e2 in edges:
                    edges.remove(e2)
                else:
                    break

        sides += 1

    return sides


@puzzle.solution_a
def solve_p1(data):
    return sum((len(z) * len(p) for z, p in get_regions(parse_grid(data))))


@puzzle.solution_b
def solve_p2(data):
    return sum((len(z) * count_sides(p) for z, p in get_regions(parse_grid(data))))


puzzle.check_solutions()
