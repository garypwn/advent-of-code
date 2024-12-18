import re
from collections.abc import Generator
from typing import Pattern


def find_in_line(data: str, pattern: Pattern | str) -> Generator[Generator[str]]:
    if not isinstance(pattern, Pattern):
        pattern = re.compile(pattern)
    for line in data.split('\n'):
        yield (s.group(0) for s in re.finditer(pattern, line))


def integers(data: str, negative: bool = True) -> Generator[Generator[int]]:
    pattern = r"(?:-|\b)\d+\b" if negative else r"\b(\d+)\b"
    for line in find_in_line(data, pattern):
        yield (int(s) for s in line)


def floats(data: str) -> Generator[Generator[float]]:
    pattern = r"(?:-|\b)\d+(?:\.\d+)?\b"
    for line in find_in_line(data, pattern):
        yield (float(s) for s in line)
