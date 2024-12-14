import math
import operator
import re
from functools import reduce
from itertools import product

import numpy as np
from numpy.ma.extras import average

from utils import tuples
from utils.aocd_solutions import Puzzle
from utils.grid_2d import coordinates_to_grid

puzzle = Puzzle(2024, 14)


def parse(data):
    pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    for m in (pattern.match(line) for line in data.split('\n')):
        p1, p2, v1, v2 = (int(i) for i in m.groups())
        yield (p1, p2), (v1, v2)


def step(robots, bounds, steps=1):
    for robot in robots:
        p, v = robot
        yield tuples.mod(tuples.add(p, tuples.scale(v, steps)), bounds), v


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
def solve_p2(data, bounds=(101, 103), verify_ct=0):
    robots = list(parse(data))

    def density_x(a):
        for i in range(a.shape[0]):
            yield np.count_nonzero(a[i, :])

    def density_y(a):
        for i in range(a.shape[1]):
            yield np.count_nonzero(a[:, i])

    arr = coordinates_to_grid([(p, 1) for p, _ in robots])
    avg_density_x = sum(density_x(arr)) / arr.shape[0]
    avg_density_y = sum(density_y(arr)) / arr.shape[0]

    offset_x = None
    period_x = None
    verify_x = 0

    offset_y = None
    period_y = None
    verify_y = 0

    for n in range(1, 100000):
        robots = list(step(robots, bounds))
        arr = coordinates_to_grid([(p, 1) for p, _ in robots])

        tgt_x = max(density_x(arr))
        tgt_y = max(density_y(arr))

        if tgt_x > avg_density_x * 3.5:
            if not offset_x:
                offset_x = n
            elif not period_x:
                period_x = n - offset_x
            else:
                assert n % period_x == offset_x
                verify_x += 1

        if tgt_y > avg_density_y * 3:
            if not offset_y:
                offset_y = n
            elif not period_y:
                period_y = n - offset_y
            else:
                assert n % period_y == offset_y
                verify_y += 1

        if period_x and period_y and verify_x == verify_ct and verify_y == verify_ct:
            break

    # Check periods are coprime
    assert math.gcd(period_y, period_x) == 1

    # We can solve for the time of convergence with the Chinese Remainder Theorem
    return ((-offset_x + offset_y) * pow(period_x, -1, period_y) % period_y) * period_x + offset_x


puzzle.check_examples((11, 7))
puzzle.check_solutions()
