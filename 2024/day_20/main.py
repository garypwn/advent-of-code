from functools import reduce
from itertools import product

from utils import tuples
from utils.aocd_solutions import Puzzle
from utils.grid_2d import grid_to_coordinates, DIRECTIONS, DIRECTIONS_DIAG, DIRECTIONS_V, UP, RIGHT
from utils.vector import Vector2

puzzle = Puzzle(2024, 20)


def get_path(pts):
    pt, = pts['E']
    start, = pts['S']
    last = None
    path = dict()  # {pt: distance to end}
    i = 0

    while True:
        path[pt] = i
        i += 1
        for d in DIRECTIONS:
            tgt = pt + d
            if tgt != last and (tgt in pts['.'] or tgt == start):
                last = pt
                pt = tgt
                break
        else:
            return path


def get_cheats(path, cutoff=100, cheat_lengths=None):
    if cheat_lengths is None:
        cheat_lengths = [2]
    cheats = dict()  # {(start, end): savings}
    cheat_destinations = set()
    for i in cheat_lengths:
        for j in range(i + 1):
            x, y = tuples.mul((Vector2(RIGHT), Vector2(UP)), (j, i - j))
            tgt = x + y
            cheat_destinations |= {(tgt * sign, i) for sign in product((1, -1), (1, -1))}

    for pt, dist in path.items():
        for d, s in cheat_destinations:
            tgt = pt + d
            if tgt in path:
                savings = path[pt] - path[tgt] - s
                if savings >= cutoff:
                    cheats[pt, tgt] = savings
    return cheats


@puzzle.solution_a
def solve_p1(data, cutoff=100):
    pts = grid_to_coordinates(data.split('\n'), '#')
    path = get_path(pts)
    cheats = get_cheats(path, cutoff)
    return len(cheats)


@puzzle.solution_b
def solve_p2(data, cutoff=100):
    pts = grid_to_coordinates(data.split('\n'), '#')
    path = get_path(pts)
    cheats = get_cheats(path, cutoff, range(1, 21))
    return len(cheats)


puzzle.check_examples(30)
puzzle.check_solutions()
