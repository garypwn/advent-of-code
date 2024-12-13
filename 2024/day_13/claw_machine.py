import re
import sys
from math import isclose

from utils import tuples
from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2024, 13)


def parse(data):
    pattern = re.compile(r"\+(\d+).*\+(\d+)\n.*\+(\d+).*\+(\d+)\n.*=(\d+).*=(\d+)")
    for block in data.split('\n\n'):
        yield tuple(int(s) for s in pattern.search(block).groups())


# Slow brute force solution that I'm not using, but I'm leaving here for the sweet memories
def prize_bf(m, max_presses=101):
    b1, b2, tgt = (m[0], m[1]), (m[2], m[3]), (m[4], m[5])
    cheapest = None

    for n in range(max_presses if max_presses else min(*tuples.floordiv(tgt, b1)) + 1):
        for m in range(max_presses if max_presses else min(*tuples.floordiv(tgt, b2)) + 1):

            result = tuples.add(tuples.scale(b1, n), tuples.scale(b2, m))
            if result == (0, 0):
                continue

            if any(r > t for r, t in zip(result, tgt)):
                # We've broken the bank
                break

            if tuples.mod(tgt, result) == (0, 0):
                scale = tgt[0] // result[0]
                if scale * n > max_presses or scale * m > max_presses:
                    continue
                cost = scale * (3 * n + m)
                cheapest = min(cost, cheapest) if cheapest else cost

    return cheapest if cheapest else 0


# Obtained by solving the system of equations nx1 + mx2 = xt and ny1 + my2 = yt
def prize_fast(m, t_offset=0):
    x1, y1, x2, y2, xt, yt = m
    xt += t_offset
    yt += t_offset

    m = int((yt * x1 - y1 * xt) / (x1 * y2 - y1 * x2))
    n = int((xt - m * x2) / x1)

    if n * x1 + m * x2 == xt and n * y1 + m * y2 == yt:
        return 3 * int(n) + int(m)
    return 0


@puzzle.solution_a
def solve_p1(data):
    return sum(prize_fast(m) for m in parse(data))


@puzzle.solution_b
def solve_p2(data):
    return sum(prize_fast(m, 10000000000000) for m in parse(data))


puzzle.check_solutions()
