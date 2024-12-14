import operator
import re
from functools import reduce
from itertools import product

import numpy as np

from utils import tuples
from utils.aocd_solutions import Puzzle
from utils.grid_2d import coordinates_to_grid

puzzle = Puzzle(2024, 14)


def parse(data):
    pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    for m in (pattern.match(line) for line in data.split('\n')):
        p1, p2, v1, v2 = (int(i) for i in m.groups())
        yield (p1, p2), (v1, v2)


def step(robots, bounds):
    for robot in robots:
        p, v = robot
        yield tuples.mod(tuples.add(p, v), bounds), v


def quadrants(robots, bounds):
    mx, my = (bound // 2 for bound in bounds)
    quads = {(bool(a), bool(b)): 0 for a, b in product(range(2), range(2))}

    for (x, y), _ in robots:
        if x == mx or y == my:
            continue
        quads[(x <= mx, y <= my)] += 1

    return quads


@puzzle.solution_a
def solve_p1(data, bounds=(101, 103)):
    robots = parse(data)
    for _ in range(100):
        robots = list(step(robots, bounds))

    quads = quadrants(robots, bounds)
    return reduce(operator.mul, quads.values(), 1)


@puzzle.solution_b
def solve_p2(data, bounds=(101, 103)):
    # We observed after printing out a lot of patterns that there are often partial lines at y=30, y=60 and x=37, x=69
    robots = parse(data)

    avg = None

    for n in range(100000):
        robots = list(step(robots, bounds))
        arr = coordinates_to_grid([(p, 1) for p, _ in robots])

        bots = np.count_nonzero(arr[:, 37])
        bots += np.count_nonzero(arr[:, 69])
        bots += np.count_nonzero(arr[30])
        bots += np.count_nonzero(arr[70])

        avg = bots if avg is None else (avg * (n - 1) + bots) / n

        # We're looking for far fewer bots around the outside than average
        if bots >= avg * 5:

            print(f"\n\n Loop #{n + 1}.")
            arr = np.transpose(arr)
            for line in arr:
                print(''.join(('X' if x == 1 else ' ' for x in line)))

            return n + 1


puzzle.check_examples((11, 7))
puzzle.check_solutions()
