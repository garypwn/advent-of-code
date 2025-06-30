from itertools import product

from utils import parser
from utils.aocd_solutions import Puzzle
from utils.ranges import RangeSet

puzzle = Puzzle(2022, 15)


@puzzle.solution_a
def solve_p1(data, target=2000000):
    covered = RangeSet()  # positions in the target row covered by a sensor
    beacons_in_row = set()  # aoc seems to not count beacons already in the row toward the answer
    for sx, sy, bx, by in parser.integers(data):
        beacon_dist = abs(bx - sx) + abs(by - sy)
        beacon_dist -= abs(sy - target)  # deduct the difference to the target row
        if by == target:
            beacons_in_row.add((bx, by))
        if beacon_dist > 0:
            covered.add((sx - beacon_dist, sx + beacon_dist + 1))

    return len(covered) - len(beacons_in_row)


@puzzle.solution_b
def solve_p2(data, midpoint=2000000):
    # Idea: the result will be bounded by 4 lines
    # one pair with slope -1, and one pair with slope 1.
    # These lines will have a separation of 1.
    # Edge case: maybe it will be one or two lines squishing the result against the square arena boundary.

    bounds = (0, midpoint * 2)  # The arena

    # Our four boundary types. If the lines are mx+b, we're storing the b
    # such that for a pair of lines, geq<result<lt.
    # The first index is the slope direction and the second is the boundary direction in (1, -1) order.
    intercepts = (gt_p, lt_p), (gt_n, lt_n) = (set(), set()), (set(), set())
    sensors = set()

    for sx, sy, bx, by in parser.integers(data):
        dist = abs(bx - sx) + abs(by - sy)  # range that no beacons can be present
        sensors.add((sx, sy, dist))
        for slope, ss in zip((1, -1), intercepts):
            for d, s in zip((1, -1), ss):
                b = sy + d * dist - slope * sx  # the intercept
                s.add(b)

    # Now we look through line sandwiched between an upper and lower bound
    # And we look eat each intersection between a positive and negative slope line. This is O(n^2).
    # But realistically there's only going to be a small portion of bounds that are exactly 2 apart.
    # Then for each of those points, we throw it away if it is in range of a beacon. This is O(n).
    # So the whole solution is O(n^3) at worst.
    results = set()
    for pos, neg in product(filter(lambda i: i + 2 in lt_p, gt_p), filter(lambda j: j + 2 in lt_n, gt_n)):
        y = (pos + neg) // 2 + 1
        x = y - pos - 1
        if all(bounds[0] <= p <= bounds[1] for p in (x, y)):
            if all(abs(x - sx) + abs(y - sy) > dist for sx, sy, dist in sensors):
                results.add((x, y))

    if len(results) == 1:
        # This solution hinges on the fact that there is exactly one solution to each puzzle.
        # If there were multiple spots the beacon could be, some might not be sandwiched between two bounds.
        x, y = results.pop()
        return 4000000 * x + y


puzzle.check_examples(10)
puzzle.check_solutions()
