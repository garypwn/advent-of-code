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


def manhattan_dist(universe, pts, x_size):
    ((x1, y1), (x2, y2)) = pts
    zone = universe[min(x1, x2):max(x1, x2) + 1, min(y1, y2):max(y1, y2) + 1]

    distance = -2

    for i in range(2):
        counts = np.unique(np.moveaxis(zone, i, 0)[0], return_counts=True)
        for c, n in zip(counts[0], counts[1]):
            if c == 'x':
                distance += x_size * n
            else:
                distance += n

    return distance


def solve(universe, x_size):
    total = 0
    g = galaxies(universe)
    for pts in itertools.combinations(g, 2):
        total += manhattan_dist(universe, pts, x_size)

    return total
