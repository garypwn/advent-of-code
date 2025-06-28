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


puzzle.check_examples(10)
puzzle.check_solutions()
