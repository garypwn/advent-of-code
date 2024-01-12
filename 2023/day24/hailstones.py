import itertools
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

    processed = np.ndarray([stones.shape[0], 2, 3], dtype=stones.dtype)  # [Hailstone, (m, w), (t, y, z)]
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


def read_input(input_lines: Iterable[str], dtype):
    # Creates arrays of u (initial position) and v (velocity) vectors
    # Returns a 3d numpy array of all hailstones in the input

    lines = [line for line in input_lines]
    arr = np.ndarray([len(lines), 2, 3], dtype=dtype)  # [Hailstone, (position, speed), (x, y, z)]
    for i, line in enumerate(lines):
        for j, part in enumerate(line.split('@')):
            arr[i, j] = [tok.strip() for tok in part.split(',')]

    return arr


class Hailstones:
    # Solver class for the hailstone problem. Tracks inputted hailstones, and the experiment boundary.

    def __init__(self, lines: Iterable[str], lower=200000000000000, upper=400000000000000, dtype=np.double):
        self.dtype = dtype
        self.stones = read_input(lines, dtype)
        self.proc = None
        self.lower = lower
        self.upper = upper

    def get_intersection(self, i, j, ignore_z):
        # Takes two indices i and j in the Hailstone array and checks returns where they intersect as an (x,y,z) tuple.
        # Or None if they never intersect.

        if self.proc is None:
            self.proc = preprocess(self.stones)

        try:
            x, y = tuple(solve_linalg(self.proc[i], self.proc[j]).ravel())
            r = (x, y)
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

        # Solve for z
        if not ignore_z:
            z = self.proc[i, 0, 2] * x + self.proc[i, 1, 2]
            r = (x, y, z)

        return r

    def find_intersections(self, ignore_z=True):
        # Returns a list containing the locations of all hailstone intersections.
        # O(n^2) operation that compares each hailstone against each other hailstone
        intersections = []
        for i in range(len(self.stones)):
            for j in range(i + 1, len(self.stones)):
                if (r := self.get_intersection(i, j, ignore_z)) is not None:
                    intersections.append(r)

        return intersections

    def find_parallel_hailstones(self):
        # Returns a list of parallel hailstones, if there are any
        pairs = []
        for stones in itertools.combinations(self.stones, 2):

            stone_1, stone_2 = (stone[1] for stone in stones)
            cross = np.cross(stone_1, stone_2)
            if np.isclose(cross, np.zeros(3), atol=1).all():
                pairs.append(stones)

        return pairs
