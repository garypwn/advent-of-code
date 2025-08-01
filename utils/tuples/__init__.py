"""
Tools for performing element-wise operations on tuples of hashable types
"""
from collections.abc import Sequence
from functools import cache
from typing import TypeVar, Tuple

T = TypeVar('T', int, float)

@cache
def add(t1: Sequence[T], t2: Sequence[T]) -> Tuple[T, ...]:
    """Element-wise add two tuples of the same length"""
    return tuple(a + b for a, b in zip(t1, t2))


@cache
def sub (t1: Sequence[T], t2: Sequence[T]) -> Tuple[T, ...]:
    """Element-wise subtract two tuples of the same length"""
    return tuple(a - b for a, b in zip(t1, t2))


@cache
def neg(t: Sequence[T]) -> Tuple[T, ...]:
    """Negate all elements in a tuple"""
    return tuple(-a for a in t)


@cache
def dot(t1: Sequence[T], t2: Tuple[T, ...]) -> T:
    """Compute the dot product of two tuples of the same length"""
    return sum(a * b for a, b in zip(t1, t2))


@cache
def mod(t1: Sequence[T], t2: Sequence[T]) -> Tuple[T, ...]:
    """Compute the modulo of two tuples of the same length"""
    return tuple(a % b for a, b in zip(t1, t2))


@cache
def mul(t1: Sequence[T], t2: Sequence[T]) -> Tuple[T, ...]:
    """Compute the product of two tuples of the same length"""
    return tuple(a * b for a, b in zip(t1, t2))


@cache
def floordiv(t1: Sequence[T], t2: Sequence[T]) -> Tuple[T, ...]:
    """Compute integer dividend of two tuples of the same length"""
    return tuple(a // b for a, b in zip(t1, t2))


@cache
def scale(t: Sequence[T], s: T) -> Tuple[T, ...]:
    """Multiply a tuple t by a scalar s"""
    return tuple(a * s for a in t)


@cache
def sgn(t: Sequence[T]) -> Tuple[T, ...]:
    """Applies the sign() function to each scalar"""
    return tuple((x > 0) - (x < 0) for x in t)
