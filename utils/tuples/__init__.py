from functools import cache


@cache
def add(t1: tuple, t2: tuple) -> tuple:
    return tuple(a + b for a, b in zip(t1, t2))


@cache
def sub(t1: tuple, t2: tuple) -> tuple:
    return tuple(a - b for a, b in zip(t1, t2))


@cache
def neg(t: tuple) -> tuple:
    return tuple(-a for a in t)
