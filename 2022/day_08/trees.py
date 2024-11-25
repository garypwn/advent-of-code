from functools import reduce

import numpy as np

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2022, 8)

def map_visible(data):
    trees = np.array([[int(s) for s in line] for line in data.split('\n')])
    directions = [np.rot90(trees.copy(), k) for k in range(4)]
    for view in directions:
        for row in view:
            tallest = -1
            for i, t in enumerate(row):
                if t > tallest:
                    tallest = t
                    row[i] = 1
                else:
                    row[i] = 0

    directions = [np.rot90(direction, -i) == 1 for i, direction in enumerate(directions)]
    return reduce(lambda x, y: x | y, directions)

@puzzle.solution_a
def count_visible(data):
    return np.count_nonzero(map_visible(data))

@puzzle.solution_b
def scenic_scores(data):
    trees = np.array([[int(s) for s in line] for line in data.split('\n')])
    scores = np.ones(trees.shape, dtype=int)
    for trees_view, scores_view in [(np.rot90(trees, k), np.rot90(scores, k)) for k in range(4)]:
        for i, row in enumerate(trees_view):
            distances = [0]*10
            for j, t in enumerate(row):
                scores_view[i,j] *= distances[t]
                distances[:t+1] = [1]*(t+1)
                distances[t+1:] = [x+1 for x in distances[t+1:]]
    return scores.ravel().max()

puzzle.check_examples()
puzzle.check_solutions()