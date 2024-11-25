import re

from utils.aocd_solutions import Puzzle
from utils.grid_2d import DIRECTION_DICT
from utils.tuples import add, sub

puzzle = Puzzle(2022, 9)


def sgn(x):
    return (x > 0) - (x < 0)


class Rope:
    sections: list[tuple[int, int]]
    tail_visited: set[tuple[int, int]]

    def __init__(self, length):
        self.tail_visited = {(0, 0)}
        self.sections = [(0, 0)] * length

    def move_head(self, direction):
        self.sections[0] = add(self.sections[0], DIRECTION_DICT[direction])

        for i in range(1, len(self.sections)):
            delta = sub(self.sections[i - 1], self.sections[i])
            if -1 <= delta[0] <= 1 and -1 <= delta[1] <= 1:
                move = (0, 0)
            elif abs(delta[0]) == 2 and delta[1] == 0:
                move = (sgn(delta[0]), 0)
            elif delta[0] == 0 and abs(delta[1]) == 2:
                move = (0, sgn(delta[1]))
            else:
                assert abs(delta[0]) > 0 and abs(delta[1]) > 0
                move = tuple(sgn(x) for x in delta)
            self.sections[i] = add(self.sections[i], move)

        self.tail_visited.add(self.sections[-1])


def count_visited(data, length):
    rope = Rope(length)
    pattern = re.compile(r"([UDLR]) (\d+)")
    for line in data.split('\n'):
        d, n = pattern.match(line).groups()
        for _ in range(int(n)):
            rope.move_head(d)

    return len(rope.tail_visited)


@puzzle.solution_a
def solve_p1(data):
    return count_visited(data, 2)


@puzzle.solution_b
def solve_p2(data):
    return count_visited(data, 10)


puzzle.check_examples()
puzzle.check_solutions()
