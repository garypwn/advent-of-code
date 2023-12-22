from __future__ import annotations
from typing import Iterable

import numpy as np

directions = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}


class Garden:
    # Represents a single state

    grid: np.ndarray  # The main grid. Coordinates are (y, x).

    def __copy__(self):
        c = Garden()
        c.grid = self.grid.__copy__()
        return c

    def __init__(self, lines: Iterable[str]):
        if isinstance(lines, np.ndarray):
            self.grid = lines
            return

        g = []
        for line in lines:
            line = line.strip()
            assert (g == [] or len(line) == len(g[0]))  # Grid should be a proper rectangle
            g.append([c for c in line.encode("utf-8")])

        self.grid = np.array(g, dtype='b')

    def __str__(self):
        return '\n'.join(row.tobytes().decode('utf-8') for row in self.grid)

    def in_bounds(self, y, x):

        if y < 0:
            return False
        if x < 0:
            return False
        if y >= len(self.grid):
            return False
        if x >= len(self.grid[0]):
            return False

        return True

    def step(self) -> Garden:
        # Returns the garden after taking a step

        it = np.nditer(self.grid, flags=['multi_index'])
        grid = self.grid.copy()
        for x in it:

            # Check cell type
            match chr(x):
                case '#' | '.':  # Rocks or garden plots
                    continue
                case 'O' | 'S':  # Current location(s)
                    pass
                case _:
                    raise ValueError(f"Invalid garden character: {x}")

            # If the elf is here, assign possible step locations with 'X'
            for d in directions.values():
                idx = it.multi_index
                t = (d[0] + idx[0], d[1] + idx[1])

                # Check if the target is in bounds
                if not self.in_bounds(*t):
                    continue

                # Check if the target is a rock
                if chr(self.grid[t]) == "#":
                    continue

                grid[t] = ord('X')

        # At this point, the elf's locations are marked with 'O' (or 'S' if this is the starting step)
        # and the new possible locations are marked with 'X', overwriting any 'O' or 'S'.
        # We can just delete remaining 'O' cells and change 'S' cells to 'O'.
        with np.nditer(grid, op_flags=['readwrite']) as it:
            for x in it:
                match chr(x):
                    case 'O' | 'S':
                        x[...] = ord('.')
                    case 'X':
                        x[...] = ord('O')
                    case _:
                        continue

        return Garden(grid)

    def count_destinations(self) -> int:
        # Counts the number of 'O' or 'S' cells in the garden.

        return np.count_nonzero(self.grid == ord('O')) + np.count_nonzero(self.grid == ord('S'))
