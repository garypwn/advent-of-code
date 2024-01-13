from enum import Enum
import re
from typing import Iterable

colors = {"red", "green", "blue"}
_pattern = re.compile(r"\s*(\d+)\s*(\w+)")


class CubeGame:
    sets: list[dict]

    def __init__(self, line: str):
        self.sets = []
        for substr in line.split(';'):
            s = {color: 0 for color in colors}
            for set_str in substr.split(','):
                n, color = _pattern.match(set_str).groups()
                color = color.lower()
                if color not in colors:
                    raise ValueError()
                s[color] = n

            self.sets.append(s)

    def max(self):
        return {color: max([int(s[color]) for s in self.sets]) for color in colors}

    def check_limit(self, limits):
        maxes = self.max()
        for color in colors:
            if maxes[color] > limits[color]:
                return False
        return True

    def min_power(self):
        maxes = self.max()
        prod = 1
        for n in maxes.values():
            prod *= n

        return prod


def create_games(lines: Iterable[str]):
    games = []
    for line in lines:
        seqs = line.split(':')
        games.append(CubeGame(seqs[1]))

    return games
