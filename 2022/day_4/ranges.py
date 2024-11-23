import re

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2022, 4)

def parse_lines(data):
    pattern = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")
    return [[int(s) for s in pattern.match(line).groups()] for line in data.split('\n')]

def check_total_overlap(bounds):
    return bounds[0] <= bounds[2] and bounds[1] >= bounds[3] or bounds[0] >= bounds[2] and bounds[1] <= bounds[3]

@puzzle.solution_a
def count_total_overlaps(data):
    return sum([1 if check_total_overlap(b) else 0 for b in parse_lines(data)])

def check_partial_overlap(bounds):
    min1, max1, min2, max2 = bounds
    r1, r2 = range(min1, max1+1), range(min2, max2+1)
    return min1 in r2 or max1 in r2 or min2 in r1 or max2 in r1

@puzzle.solution_b
def count_partial_overlaps(data):
    return sum([1 if check_partial_overlap(b) else 0 for b in parse_lines(data)])

puzzle.check_examples()
puzzle.check_solutions()