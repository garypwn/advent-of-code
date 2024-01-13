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

    def gears(self):
        # Iterates over gears
        for i, line in enumerate(self.array):
            for col, c in enumerate(line):
                if c != '*':
                    continue

                parts = []

                for row in range(i-1, i+2):
                    if not (0 <= row < self.height):
                        continue

                    for match in _pattern.finditer(self.array[row]):
                        if match.start() - 1 <= col <= match.end():
                            parts.append(int(match.group(0)))

                # Gears have exactly 2 adjacent parts
                if len(parts) == 2:
                    yield parts[0], parts[1]