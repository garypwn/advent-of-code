from typing import Any

import numpy as np
from numpy import ndarray, dtype
from sortedcontainers import SortedSet

from utils.idx_tools import DIRECTIONS, bounds
from utils.tuples import add


def parse(lines) -> ndarray[Any, dtype[np.uint]]:
    return np.array([[int(s) for s in line.strip()] for line in lines])


class City:
    def __init__(self, lines):
        self.grid = parse(lines)

    def moves(self, idx, vert, min_len, max_len):
        # iterates over (idx, vert, cost)
        # The idea is that each there's 3 spots you could be forced to turn in each direction
        # => 12 possible moves - map bounds

        for d in DIRECTIONS:

            # Check if d matches vert
            if (d[0] == 0) == vert:
                continue

            new_idx = idx
            weight = 0
            for i in range(max_len):

                new_idx = add(new_idx, d)

                if not bounds(self.grid, new_idx):
                    break

                weight += self.grid[new_idx]
                if i < min_len - 1:
                    continue

                yield new_idx, weight

    def dijkstra(self, start=(0, 0), min_len=1, max_len=3):
        # Our graph nodes are 2 stacked grids: vertical and horizontal movement.
        # Each move we alternate.

        dists = {b: np.full_like(self.grid, 9999999999) for b in (True, False)}
        for dist in dists.values():
            dist[start] = 0

        processed = set()
        queue = SortedSet([(start, True), (start, False)], key=lambda iv: dists[iv[1]][iv[0]])

        while queue:

            idx, vert = queue.pop(0)
            d = dists[vert][idx]
            for target, weight in self.moves(idx, vert, min_len, max_len):
                n = (target, not vert)
                queue.discard(n)
                dists[not vert][target] = min(d + weight, dists[not vert][target])
                if n not in processed:
                    queue.add(n)

            processed.add((idx, vert))

        return np.fmin(*dists.values())
