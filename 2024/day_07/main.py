from functools import cache
from math import floor, log10

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2024, 7)


def parse(data):
    tests = dict()
    for line in data.split('\n'):
        r, o = line.split(':')
        tests[int(r)] = [int(s) for s in o.split()]
    return tests


@cache
def digits(n):
    return 10 ** len(str(n))


def possibly_true(result, op1, operands, p2=False):

    # Quick short circuit if the numbers are getting too high
    if op1 > result:
        return False

    if not operands:
        return result == op1

    op2 = operands[0]

    if possibly_true(result, op1 + op2, operands[1:], p2):
        return True
    if possibly_true(result, op1 * op2, operands[1:], p2):
        return True
    if p2 and possibly_true(result, digits(op2) * op1 + op2, operands[1:], p2):
        return True

    return False



@puzzle.solution_a
def solve_p1(data):
    tests = parse(data)
    return sum(r if possibly_true(r, ops[0], ops[1:]) else 0 for r, ops in tests.items())


@puzzle.solution_b
def solve_p1(data):
    tests = parse(data)
    return sum(r if possibly_true(r, ops[0], ops[1:], p2=True) else 0 for r, ops in tests.items())


puzzle.check_examples()
puzzle.check_solutions()
