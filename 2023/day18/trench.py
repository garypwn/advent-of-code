import itertools
import re

from sortedcontainers import SortedDict

# Trenches are sorted dicts (x,y): color

_directions = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0)
}


def add_wall(trench: SortedDict, start, direction, length, color=0):
    x, y = start
    pt = start
    d = _directions[direction]
    for i in range(1, length + 1):
        pt = x + i * d[0], y + i * d[1]
        trench[pt] = color

    return pt


def flood_fill(trench, seed, color=0):
    queue = {seed}
    while queue:
        pt = queue.pop()
        for d in _directions.values():
            new = pt[0] + d[0], pt[1] + d[1]
            if new not in trench:
                queue.add(new)
                trench[new] = color


_pattern = re.compile(r"^([LRUD]) (\d+) \(#(\w+)\)")


def parse(lines):
    pt = (0, 0)
    trench = SortedDict()
    trench[pt] = 0
    for line in lines:
        angle, dist, color = _pattern.match(line).groups()
        pt = add_wall(trench, pt, angle, int(dist), int(color, 16))

    return pt, trench
