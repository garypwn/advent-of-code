from itertools import product

from aocd.examples import Example

from utils import parser, tuples
from utils.aocd_solutions import Puzzle
from utils.grid_2d import DIRECTIONS, UP, LEFT, RIGHT, DOWN
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

    not_excluded = lambda p: all(abs(p[0] - xx) + abs(p[1] - xy) > xd for xx, xy, xd in sensors)

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
            if not_excluded((x, y)):
                results.add((x, y))

    if len(results) > 1:
        raise ValueError(f"Two possible solutions! {results}")

    # Extra logic for points sandwiched against the arena
    if len(results) < 1:
        # Hard check the 4 corners
        for corner in product(*2 * (bounds,)):
            if not_excluded(corner):
                results.add(corner)

    if len(results) < 1:
        # Check edge sandwiches. This is straight up O(n^3) greedy so hopefully it doesn't come to this.
        for direction, lines in zip(((0, 1), (-1, 0), (1, 0), (0, -1)), product(*intercepts)):
            for pos, neg in product(*lines):
                intersection_y, r = divmod(pos + neg, 2)
                if r != 0:
                    # Intersections halfway between two points could give valid solutions,
                    # But they would give two possibilities, which makes them outside spec. So we ignore them.
                    continue

                intersection = intersection_y - pos, intersection_y

                pt = tuples.add(intersection, direction)
                if all(bounds[0] <= p <= bounds[1] for p in pt):
                    if any(p in bounds for p in pt) and not_excluded(pt):
                        # We consider a point if it is on any arena boundary and not excluded by sensors.
                        results.add(pt)
                        break  # Short circuit if we found a viable solution.

            # Control flow shenanigans to break out of nested loop
            else:
                continue
            break

    if len(results) == 1:
        # This solution hinges on the fact that there is exactly one solution to each puzzle.
        # If there were multiple spots the beacon could be, some might not be sandwiched between two bounds.
        x, y = results.pop()
        return 4000000 * x + y


def test():
    corner_example = "Sensor at x=11, y=11: closest beacon is at x=11, y=32"
    result = solve_p2(corner_example, 10)
    print(f"Corner Example: {'Pass' if result == 0 else 'Fail'}")

    edge_example = """x=0, y=0, x=0, y=29\nx=20, y=0, x=20, y=29"""
    result = solve_p2(edge_example, 10)
    answer = 4000000 * 10 + 20
    print(f"Edge Example: {'Pass' if result == answer else 'Fail'}")


test()
puzzle.check_examples(10)
puzzle.check_solutions()
