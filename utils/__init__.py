UP = (-1, 0)
DOWN = (1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)
DIRECTIONS = {UP, DOWN, LEFT, RIGHT}


def add(t1, t2):
    return tuple(a + b for a, b in zip(t1, t2))


def sub(t1, t2):
    return tuple(a - b for a, b in zip(t1, t2))


def neg(t):
    return tuple(-a for a in t)
