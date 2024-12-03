import re

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2024, 3)


def parse_mult(data):
    for match in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)", data):
        yield int(match.group(1)) * int(match.group(2))


def parse_p2(data):
    do = True
    for match in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)", data):
        if match.group(0) == "do()":
            do = True
        elif match.group(0) == "don't()":
            do = False
        elif do:
            yield int(match.group(1)) * int(match.group(2))


@puzzle.solution_a
def product(data):
    return sum(parse_mult(data))


@puzzle.solution_b
def product(data):
    return sum(parse_p2(data))


puzzle.check_examples()
puzzle.check_solutions()
