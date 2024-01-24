import numpy as np

UP = (-1, 0)
DOWN = (1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)
DIRECTIONS = {UP, DOWN, LEFT, RIGHT}


def bounds(pt: tuple, arr: np.array) -> bool:
    return all((0 <= a < b for a, b in zip(pt, arr.shape)))
