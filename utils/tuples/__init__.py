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
