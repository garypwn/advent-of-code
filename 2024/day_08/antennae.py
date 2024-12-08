from itertools import product, pairwise

import numpy as np

from utils import tuples
from utils.aocd_solutions import Puzzle
from utils.grid_2d import chararray

puzzle = Puzzle(2024, 8)

def parse(data):
    # Dict of list of points
    grid = chararray(data.split('\n'))
    frequencies = dict()
    for i, j in product(*[range(s) for s in grid.shape]):
        c = grid[i,j]
        if c == '.':
            continue

        if c not in frequencies:
            frequencies[c] = set()

        frequencies[c].add((i,j))

    return frequencies, grid.shape

def find_antinodes(frequencies, bounds, resonate=False):
    antinodes = {f: set() for f in frequencies.keys()}
    for freq, antennae in frequencies.items():
        for a, b in product(antennae, antennae):
            if a == b:
                continue
            delta = tuples.sub(a, b)

            if resonate:
                antinodes[freq] |= {a, b}

            while True:
                a = tuples.add(a, delta)
                if not all(0 <= p < t for p, t in zip(a, bounds)):
                    break
                antinodes[freq].add(a)
                if not resonate:
                    break

            while True:
                b = tuples.sub(b, delta)
                if not all(0 <= p < t for p, t in zip(b, bounds)):
                    break
                antinodes[freq].add(b)
                if not resonate:
                    break

    return antinodes

@puzzle.solution_a
def solve_p1(data):
    pts = set()
    for s in find_antinodes(*parse(data)).values():
        pts |= s
    return len(pts)

@puzzle.solution_b
def solve_p1(data):
    f, b = parse(data)
    pts = set()
    for s in find_antinodes(f, b, True).values():
        pts |= s
    return len(pts)



puzzle.check_examples()
puzzle.check_solutions()