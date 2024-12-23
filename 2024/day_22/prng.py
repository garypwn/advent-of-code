import numpy as np

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2024, 22)


def parse(data):
    return np.asarray([int(s) for s in data.split('\n')], dtype=np.int32)


def prng(n):
    n ^= n << 6  # Equivalent to n *= 64
    n &= 16777215  # Equivalent to n %= 16777216 since it's 2**24
    n ^= n >> 5
    n &= 16777215
    n ^= n << 11
    n &= 16777215
    return n


@puzzle.solution_a
def solve_p1(data):
    nums = parse(data)
    for _ in range(2000):
        nums = prng(nums)
    return sum(int(n) for n in nums)


puzzle.check_solutions()
