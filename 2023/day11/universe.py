import itertools

import numpy as np


def parse(lines):
    return np.asarray([[s for s in line.strip()] for line in lines])


def expand(universe, axis):
    result = np.moveaxis(universe, axis, 0)
    for i, row in enumerate(result):
        if (np.unique(row) != '#').all():
            result[i] = np.full(row.shape, 'x')

    return np.moveaxis(result, 0, axis)


def galaxies(universe):
    pts = np.nonzero(universe == '#')
    return zip(pts[0], pts[1])


def manhattan_dist(universe_sized, pts, x_size):

    ((x1, y1), (x2, y2)) = pts
    zone = universe_sized[min(x1, x2):max(x1, x2) + 1, min(y1, y2):max(y1, y2) + 1]

    distance = -2

    distance += sum(zone[:, 0])
    distance += sum(zone[0, :])

    return int(distance)


def solve(universe, x_size):
    total = 0
    g = galaxies(universe)
    sized = (universe == 'x') * (x_size - 1) + 1
    for pts in itertools.combinations(g, 2):
        total += manhattan_dist(sized, pts, x_size)

    return total
