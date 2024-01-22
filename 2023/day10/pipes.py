import numpy as np

_pipes = {
    # Coordinates are (-y, x)
    '|': ((1, 0), (-1, 0)),
    '-': ((0, 1), (0, -1)),
    'L': ((-1, 0), (0, 1)),
    'J': ((-1, 0), (0, -1)),
    '7': ((1, 0), (0, -1)),
    'F': ((1, 0), (0, 1)),
    'S': ((1, 0), (-1, 0), (0, 1), (0, -1)),
    '.': None
}


def add(t1, t2):
    return tuple(a + b for a, b in zip(t1, t2))


def sub(t1, t2):
    return tuple(a - b for a, b in zip(t1, t2))


def neg(t):
    return tuple(-a for a in t)


class Pipes:
    grid: np.array

    def __init__(self, lines):
        self.grid = np.asarray([[s for s in line] for line in lines])

    def start(self):
        return tuple(a.item() for a in np.nonzero(self.grid == 'S'))

    def follow(self, curr, last):
        for d in _pipes[self.grid[curr].item()]:
            p = add(curr, d)
            if p == last:
                continue
            if neg(d) in _pipes[self.grid[p]]:
                return p

    def loop(self):
        points = [self.start()]
        while True:
            p = self.follow(points[-1], points[-2] if len(points) > 1 else None)
            if p == points[0]:
                return points

            points.append(p)

