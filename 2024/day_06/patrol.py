from copy import copy

import numpy as np

from utils import tuples
from utils.aocd_solutions import Puzzle
from utils.grid_2d import UP, CW, DIRECTIONS

puzzle = Puzzle(2024, 6)


def parse(data):
    return np.asarray([[ord(s) for s in row] for row in data.split('\n')])


def path(grid, pos=None, direction=None, visited_states=None, visited=None, find_blockers=False):
    if not pos:
        pos = tuple(n[0] for n in np.where(grid == ord('^')))
    if not direction:
        direction = UP
    if visited_states is None:
        visited_states = set()
    if not visited:
        visited = set()

    potential_blockers = set()
    start_pos = pos

    while True:

        state = pos + (DIRECTIONS.index(direction),)

        # This means we're in a loop
        if state in visited_states:
            return None

        visited_states.add(state)
        if find_blockers:
            visited.add(pos)

        tgt = tuples.add(pos, direction)

        # leaving the area
        if not all((0 <= n < s for n, s in zip(tgt, grid.shape))):
            break

        # hit a wall
        elif grid[tgt] not in (46, 94):
            direction = CW[direction]

        # No blocker
        else:
            if find_blockers and tgt not in potential_blockers and tgt != start_pos and tgt not in visited:

                vs_cp = copy(visited_states)
                vs_cp.remove(state)

                # We will mutate grid and remember to un-mutate it when we're done
                stored_val = grid[tgt]
                grid[tgt] = 35
                if not path(grid, pos, direction, visited_states=vs_cp, visited = visited):
                    potential_blockers.add(tgt)

                grid[tgt] = stored_val

            pos = tgt

    return visited_states, potential_blockers


@puzzle.solution_a
def solve_p1(data):
    grid = parse(data)
    visited, _ = path(grid)
    return len(set((x, y) for x, y, _ in visited))


@puzzle.solution_b
def solve_p2(data):
    grid = parse(data)
    visited, blockers = path(grid, find_blockers=True)
    return len(blockers)


puzzle.check_examples()
puzzle.check_solutions()
