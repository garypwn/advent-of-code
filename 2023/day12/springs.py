import re
from functools import cache


def parse(lines):
    for line in lines:
        springs, groups = line.split()
        groups = [int(g) for g in groups.split(',')]
        yield springs, tuple(groups)


@cache
def arrangements(line: str, groups: tuple):
    if not groups:
        return 0 if '#' in line else 1

    n = groups[0]
    count = 0

    # Iterate over each spot the first group could fit
    for match in re.finditer(f"(?:(?<=^)|(?<=[?.]))(?=([?#]{{{n}}})($|[?.]))", line):
        pos = match.start(0)
        before = line[:pos]
        if '#' in before:
            break

        if match[2] != '':
            remainder = line[pos + n + 1:]
        else:
            remainder = ''

        count += arrangements(remainder, groups[1:])

    return count


def unfold(lines):
    for line, groups in lines:
        yield '?'.join([line]*5), groups * 5
