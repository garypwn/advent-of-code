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
