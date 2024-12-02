from itertools import pairwise

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2024, 2)


def parse(data):
    return [[int(n) for n in line.split()] for line in data.split('\n')]


@puzzle.solution_a
def list_safety(data):
    lists = parse(data)

    def list_check(l):
        deltas = [abs(a - b) for a, b in pairwise(l)]
        order = sorted(l)
        return min(deltas) >= 1 and max(deltas) <= 3 and (l == order or l[::-1] == order)

    return len(list(filter(list_check, lists)))


@puzzle.solution_b
def list_safety_b(data):
    lists = parse(data)

    def list_check(l, cmp, problem_dampener=False):
        for i, (a, b) in enumerate(pairwise(l)):
            if not cmp(a, b) or not 1 <= abs(a - b) <= 3:
                if problem_dampener:
                    return list_check(l[:i] + l[i + 1:], cmp) or list_check(l[:i + 1] + l[i + 2:], cmp)
                else:
                    return False
        return True

    geq = lambda a, b: a >= b
    leq = lambda a, b: a <= b
    f = lambda l: list_check(l, geq, True) or list_check(l, leq, True)

    return len(list(filter(f, lists)))


puzzle.check_examples()
puzzle.check_solutions()
