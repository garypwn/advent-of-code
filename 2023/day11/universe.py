import itertools

import numpy as np


def parse(lines):
    return np.asarray([[s for s in line.strip()] for line in lines])


def expand(universe, axis):
    offset = 0
    result = universe
    for i, row in enumerate(np.rollaxis(universe, axis)):
        if (np.unique(row) == '.').all():
            result = np.insert(result, i + offset, row, axis=axis)
            offset += 1

    return result


def galaxies(universe):
    pts = np.nonzero(universe == '#')
    return zip(pts[0], pts[1])


def manhattan_dist(p1, p2):
    return sum(abs(b - a) for a, b in zip(p1, p2))


def solve_p1(universe):
    total = 0
    for g1, g2 in itertools.combinations(galaxies(universe), 2):
        total += manhattan_dist(g1, g2)

    return total
