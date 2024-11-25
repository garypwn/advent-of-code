from itertools import product

import igraph
import numpy as np
from igraph import Graph

from utils.aocd_solutions import Puzzle
from utils.grid_2d import DIRECTIONS_NP

puzzle = Puzzle(2022, 12)


def create_graph(data) -> (Graph, str, str):
    # Start by making a grid, grab the start and end indices, and swap them out for 'a' and 'z'.
    grid = np.asarray([[ord(s) for s in line.strip()] for line in data.split('\n')])
    start = np.where(grid == ord('S'))
    grid[start] = ord('a')
    end = np.where(grid == ord('E'))
    grid[end] = ord('z')

    def in_bounds(idx):
        return all(idx >= (0, 0)) and all(idx < grid.shape)

    # Set up our adjacency list. We convert all np objects to nice hashable strings.
    adjacency_dict = {
        str(np.asarray([x,y])):
            [str(u) for u in

             # Edges point to adjacent grid squares.
             # We filter out grid squares that are out of bounds, or where the target elevation is too high.
             filter(lambda v: in_bounds(v) and grid[tuple(v)] <= grid[x, y] + 1, [d + (x, y) for d in DIRECTIONS_NP])
             ]
        for x, y in product(range(grid.shape[0]), range(grid.shape[1]))  # All indices in the grid
    }

    return igraph.Graph.ListDict(adjacency_dict, directed=True), grid, str(np.asarray(start).ravel()), str(
        np.asarray(end).ravel())


@puzzle.solution_a
def shortest_path(data):
    g, _, start, end = create_graph(data)
    path = g.get_shortest_path(start, end, output='epath')
    return len(path)

@puzzle.solution_b
def shortest_path_p2(data):
    g, grid, _, end = create_graph(data)
    starts = [str(i) for i in np.argwhere(grid == ord('a'))]

    # For whatever reason this returns a list of lists, so we just unwrap it
    distances = [l[0] for l in g.distances(starts, end)]
    return min(distances)

puzzle.check_examples()
puzzle.check_solutions()
