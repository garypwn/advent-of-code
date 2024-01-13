import itertools
import re
from typing import Iterable

_pattern = re.compile(r"\b\d+\b")


class Machine:

    def __init__(self, lines: Iterable[str]):
        self.array = [line.strip() for line in lines]
        self.height = len(self.array)
        self.width = len(self.array[0])

    def __iter__(self):
        # Iterates over part numbers

        for i, line in enumerate(self.array):
            for match in _pattern.finditer(line):
                start = match.start()
                end = match.end()

                # Find the targets to look for symbols in
                for row, col in itertools.product(range(i - 1, i + 2), range(start - 1, end + 1)):

                    # Bounds check
                    if not (0 <= row < self.height):
                        continue
                    if not (0 <= col < self.width):
                        continue

                    if self.array[row][col] in '@#$%&*-=+/':
                        yield int(match.group(0))

