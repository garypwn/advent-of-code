import collections
from itertools import cycle

import numpy as np

from utils.aocd_solutions import Puzzle
from utils.cycles import CycleFinder
from utils.tuples import add

puzzle = Puzzle(2022, 17)

# Rocks appear so that their left edge is 2 units from the edge of the field (at [2,0])
# and their bottom edge is 3 units above the floor
# So our "anchor" is the bottom left corner of the object
ROCKS = (
    ((0, 0), (1, 0), (2, 0), (3, 0)),  # Horizontal line
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),  # Cross
    ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),  # Bend
    ((0, 0), (0, 1), (0, 2), (0, 3)),  # Vertical line
    ((0, 0), (0, 1), (1, 0), (1, 1))  # Square
)


def transform(rock, t):
    return tuple(add(pt, t) for pt in rock)


def collides(rock, field):
    for pt in rock:
        if not 0 <= pt[0] < 7:
            return True
        if pt[1] < 0:
            return True
        if pt in field:
            return True
    return False


def drop_rock(rock, field, height, wind):
    rock = transform(rock, (2, height + 3))

    while True:

        # Air jet
        new_rock = transform(rock, (next(wind), 0))
        if not collides(new_rock, field):
            rock = new_rock

        # Fall
        new_rock = transform(rock, (0, -1))
        if collides(new_rock, field):
            field.update(rock)
            break

        rock = new_rock

    new_h = max(p[1] for p in rock) + 1
    return max(height, new_h), rock


def draw(field, h):
    arr = np.full((7, h), '.')
    for pt in field:
        arr[pt] = '#'
    arr = np.rot90(arr)
    return '\n'.join(''.join(line) for line in arr)


def _parse_direction(s):
    return -1 if s == '<' else 1


class WindIter:
    def __init__(self, data, lookahead_size):
        self.it = cycle(_parse_direction(s) for s in data)
        self._lookahead = collections.deque(
            next(self.it) for _ in range(lookahead_size)) if lookahead_size > 0 else None

    def __next__(self):
        if not self._lookahead:
            return next(self.it)

        r = self._lookahead.popleft()
        self._lookahead.append(next(self.it))
        return r

    def lookahead(self):
        return tuple(self._lookahead)


@puzzle.solution_a(count=2022)
@puzzle.solution_b(count=1000000000000, p2=True)
def solve(data, count, p2=False):
    wind = WindIter(data, 3 if p2 else 0)
    field = set()
    h = 0

    depth_gauge = 7 * [0]
    cf = CycleFinder(10) if p2 else None
    for _, (i, r) in zip(range(count), cycle(enumerate(ROCKS))):
        new_h, new_rock = drop_rock(r, field, h, wind)

        if p2:
            dh = new_h - h
            old_depth = tuple(depth_gauge)
            for j, v in enumerate(depth_gauge):
                depth_gauge[j] += dh
            for pt in new_rock:
                depth_gauge[pt[0]] = min(depth_gauge[pt[0]], new_h - pt[1] - 1)

            state = hash((i, tuple(depth_gauge), old_depth, wind.lookahead()))
            cyc = cf.send(dh, state)
            if cyc:
                return cyc.accumulate(count)

        h = new_h

    return h


puzzle.check_examples()
puzzle.check_solutions()
