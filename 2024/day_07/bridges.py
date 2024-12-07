from functools import cache

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


def possibly_true(result, operands, p2=False):

    def helper(op1, i):
        # Quick short circuit if we're already too big
        if op1 > result:
            return False

        if i >= len(operands):
            return result == op1

        op2 = operands[i]

        if helper(op1 + op2, i+1):
            return True
        if helper(op1 * op2, i+1):
            return True
        if p2 and helper(digits(op2) * op1 + op2, i+1):
            return True

        return False
    return helper(operands[0], 1)


@puzzle.solution_a
def solve_p1(data):
    tests = parse(data)
    return sum(r if possibly_true(r, ops) else 0 for r, ops in tests.items())


@puzzle.solution_b
def solve_p1(data):
    tests = parse(data)
    return sum(r if possibly_true(r, ops, p2=True) else 0 for r, ops in tests.items())


puzzle.check_examples()
puzzle.check_solutions()
