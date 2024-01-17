import re
from typing import Iterable


def read_input(lines: Iterable[str]):
    times, distances = ((int(s) for s in re.findall(r"\b\d+\b", line)) for line in lines)
    return list(zip(times, distances))
