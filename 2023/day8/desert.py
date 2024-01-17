import functools
import itertools
import re
from typing import Iterable

_pattern = re.compile(r"(\w+) = \((\w+), (\w+)\)")


def read_lines(lines: Iterable[str]):
    iterator = lines.__iter__()
    path = next(iterator).strip()

    network = {}

    for line in iterator:
        match = _pattern.match(line)
        if not match:
            continue
        network[match[1]] = match[2], match[3]

    return path, network


def path_length(path, network):
    curr = 'AAA'
    count = 0

    while True:
        for c in path:
            if curr == 'ZZZ':
                return count

            curr = network[curr][0 if c == 'L' else 1]
            count += 1


def ghost_path_length(path, network):
    curr = {s for s in network.keys() if s[2] == 'A'}
    count = 0

    while True:
        for c in path:
            all_z = True
            for s in curr:
                if s[2] != 'Z':
                    all_z = False
                    break

            if all_z:
                return count

            curr = {network[s][0 if c == 'L' else 1] for s in curr}
            count += 1
