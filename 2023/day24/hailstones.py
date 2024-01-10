from collections.abc import Sequence, Iterable

import numpy as np
from numpy.linalg import LinAlgError


def solve_linalg(p1, p2):
    # Solves the linear equation for t, x, y. Remember to catch LinAlgError.
    m1, w1 = p1
    m2, w2 = p2
    A = np.asarray([[-m1[1], 1.], [-m2[1], 1.]])
    B = np.asarray([[w1[1]], [w2[1]]])
    return np.matmul(np.linalg.inv(A), B)


def check_time(p, x):
    # Check that time > 0
    m, w = p[0, 0], p[1, 0]
    t = m * x + w
    return t >= 0


def preprocess(stones: np.ndarray):
    # Creates arrays of the m and w vectors such that mx+w = [t, y, z]
    # Intermediate step for solving systems of equations

    processed = np.ndarray([stones.shape[0], 2, 3])  # [Hailstone, (m, w), (t, y, z)]
    for i, stone in enumerate(stones):
        # The M array
        processed[i, 0] = stone[1]  # velocities
        processed[i, 0, 0] = 1.
        processed[i, 0] /= stone[1, 0]

        # The W array
        processed[i, 1] = stone[0]  # positions
        processed[i, 1, 0] = 0.
        processed[i, 1] -= stone[0, 0] * processed[i, 0]

    return processed


def read_input(input_lines: Iterable[str]):
    # Creates arrays of u (initial position) and v (velocity) vectors
    # Returns a 3d numpy array of all hailstones in the input

    lines = [line for line in input_lines]
    arr = np.ndarray([len(lines), 2, 3])  # [Hailstone, (position, speed), (x, y, z)]
    for i, line in enumerate(lines):
        for j, part in enumerate(line.split('@')):
            arr[i, j] = [tok.strip() for tok in part.split(',')]

    return arr


class Hailstones:
    # Solver class for the hailstone problem. Tracks inputted hailstones, and the experiment boundary.

    def __init__(self, lines: Iterable[str], lower=200000000000000, upper=400000000000000):
        self.stones = read_input(lines)
        self.proc = preprocess(self.stones)
        self.lower = lower
        self.upper = upper

    def get_intersection(self, i, j):
        # Takes two indices i and j in the Hailstone array and checks returns where they intersect as an (x,y,z) tuple.
        # Or None if they never intersect.
        try:
            r = x, y = tuple(solve_linalg(self.proc[i], self.proc[j]).ravel())
        except LinAlgError:
            # Lines are parallel in a plane
            return None

        # Check bounds
        for n in r:
            if not self.lower <= n <= self.upper:
                return None

        # Check time
        for n in (i, j):
            if not check_time(self.proc[n], x):
                return None

        return x, y

    def find_intersections(self):
        # Returns a list containing the locations of all hailstone intersections.
        # O(n^2) operation that compares each hailstone against each other hailstone
        intersections = []
        for i in range(len(self.stones)):
            for j in range(i + 1, len(self.stones)):
                if (r := self.get_intersection(i, j)) is not None:
                    intersections.append(r)

        return intersections
