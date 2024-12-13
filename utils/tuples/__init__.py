"""
Tools for performing element-wise operations on tuples of hashable types
"""

from functools import cache
from typing import Any


@cache
def add[T](t1: tuple[T], t2: tuple[T]) -> tuple[Any, ...]:
    """Element-wise add two tuples of the same length"""
    return tuple(a + b for a, b in zip(t1, t2))


@cache
def sub[T](t1: tuple[T], t2: tuple[T]) -> tuple[Any, ...]:
    """Element-wise subtract two tuples of the same length"""
    return tuple(a - b for a, b in zip(t1, t2))


@cache
def neg[T](t: tuple[T]) -> tuple[Any, ...]:
    """Negate all elements in a tuple"""
    return tuple(-a for a in t)


@cache
def dot[T](t1: tuple[T], t2: tuple[T]) -> T:
    """Compute the dot product of two tuples of the same length"""
    return sum(a * b for a, b in zip(t1, t2))


@cache
def mod[T](t1: tuple[T], t2: tuple[T]) -> T:
    """Compute the modulo of two tuples of the same length"""
    return tuple(a % b for a, b in zip(t1, t2))


@cache
def mul[T](t1: tuple[T], t2: tuple[T]) -> T:
    """Compute the product of two tuples of the same length"""
    return tuple(a * b for a, b in zip(t1, t2))


@cache
def floordiv[T](t1: tuple[T], t2: tuple[T]) -> T:
    """Compute integer dividend of two tuples of the same length"""
    return tuple(a // b for a, b in zip(t1, t2))


@cache
def scale[T](t: tuple[T], s: T) -> T:
    """Multiply a tuple t by a scalar s"""
    return tuple(a * s for a in t)


@cache
def sgn[T](t: tuple[T]) -> T:
    """Applies the sign() function to each scalar"""
    return tuple((x > 0) - (x < 0) for x in t)
