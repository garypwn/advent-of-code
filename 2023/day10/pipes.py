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
        start = self.start()
        curr = start
        last = None
        while True:
            yield curr
            p = self.follow(curr, last)
            if p == start:
                break

            last = curr
            curr = p


def area(loop):
    # The area bounded by the inside edge of the pipes in the loop
    a = 0
    for curr, ahead in zip(loop, loop[1:] + loop[:1]):
        match sub(curr, ahead):
            case (0, 1):
                value = 1
            case (0, -1):
                value = -1
            case _:
                value = 0

        a += curr[0] * value
    return abs(a) - len(loop) // 2 + 1
