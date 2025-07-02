import re
from collections.abc import Generator
from typing import Pattern


def groups(data: str, pattern: Pattern | str) -> Generator[Generator[str]]:
    """Iterates over lines of input, matching an arbitrary pattern and yielding the match groups for the line."""
    if not isinstance(pattern, Pattern):
        pattern = re.compile(pattern)
    for line in data.split('\n'):
        yield pattern.match(line).groups()


def find_in_line(data: str, pattern: Pattern | str) -> Generator[Generator[str]]:
    """Iterates over lines of input, finding all matches for an arbitrary pattern and yielding a list of matches
    within the line."""
    if not isinstance(pattern, Pattern):
        pattern = re.compile(pattern)
    for line in data.split('\n'):
        yield (s.group(0) for s in re.finditer(pattern, line))


def integers(data: str, negative: bool = True) -> Generator[Generator[int]]:
    """Iterates over lines of input, yielding a list of all the integers in the line"""
    pattern = r"(?:-|\b)\d+\b" if negative else r"\b(\d+)\b"
    for line in find_in_line(data, pattern):
        yield (int(s) for s in line)


def floats(data: str) -> Generator[Generator[float]]:
    """Iterates over lines of input, yielding a list of all the floats in the line."""
    pattern = r"(?:-|\b)\d+(?:\.\d+)?\b"
    for line in find_in_line(data, pattern):
        yield (float(s) for s in line)
