import re

from sortedcontainers import SortedDict

# Trenches are dicts (x,y): color

_directions = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0),
    '0': (1, 0),
    '1': (0, -1),
    '2': (-1, 0),
    '3': (0, 1)
}

_ccw = {
    (0, 1): (-1, 0),
    (-1, 0): (0, -1),
    (0, -1): (1, 0),
    (1, 0): (0, 1)
}


def add_wall(trench: dict or None, start, direction, length, color=0):
    x, y = start
    pt = start
    d = _directions[direction]
    for i in range(1, length + 1):
        pt = x + i * d[0], y + i * d[1]
        if trench is not None:
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


def translate_hex(lines):
    for line in lines:
        _, _, color = _pattern.match(line).groups()
        dist = int(color.strip()[:-1], 16)
        yield dist, color.strip()[-1]


def solve_p2(move_iter, ccw=False):
    # move_iter is an iterator that yields (distance, direction)
    moves = list(move_iter)
    pt = (0, 0)
    area = 0
    for (dist, angle), (_, next_angle), (_, prev_angle) in zip(moves, moves[1:] + moves[:1], moves[-1:] + moves[:-1]):

        d = _directions[angle]
        dist += 1
        if (_directions[next_angle] == _ccw[d]) != ccw:
            dist -= 1
        if (_ccw[_directions[prev_angle]] == d) != ccw:
            dist -= 1

        area += d[1] * pt[0] * dist
        pt = tuple((p + q * dist for p, q in zip(pt, d)))

    return abs(area), pt

