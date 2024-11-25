import json
from functools import cmp_to_key
from itertools import chain

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2022, 13)

def pairs(data):
    # This can be done super easily with a json decoder
    for pair in data.split('\n\n'):
        yield [json.loads(p) for p in pair.split('\n')]

def cmp(l: list | int, r: list | int):
    # Here we implement the comparison logic set out by the puzzle
    if isinstance(l, int) and isinstance(r, int):
        return l - r
    elif isinstance(l, int):
        return cmp([l], r)
    elif isinstance(r, int):
        return cmp(l, [r])

    # Empty lists
    if len(l) == 0 and len(r) == 0:
        return 0
    elif len(l) == 0:
        return -1
    elif len(r) == 0:
        return 1

    # Lists with items
    c = cmp(l[0], r[0])
    return cmp(l[1:], r[1:]) if c == 0 else c

@puzzle.solution_a
def solve_p1(data):
    correct_indices = []
    for i, pair in enumerate(pairs(data)):
        if cmp(*pair) <= 0:
            correct_indices.append(i+1)

    return sum(correct_indices)

@puzzle.solution_b
def solve_p2(data):
    packets = list(chain(*pairs(data))) + [[[2]], [[6]]]
    packets.sort(key=cmp_to_key(cmp))

    k = 1
    for i, p in enumerate(packets):
        if p == [[2]] or p == [[6]]:
            k *= i+1

    return k

puzzle.check_examples()
puzzle.check_solutions()