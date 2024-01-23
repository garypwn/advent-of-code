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
        if '#' in line:
            return []

        return [line.replace('?', '.')]

    n = groups[0]

    results = []

    # Try to fit the first group in nicely
    for match in re.finditer(f"(?:(?<=^)|(?<=[?.]))(?=([?#]{{{n}}})($|[?.]))", line):
        pos = match.start(0)
        before = line[:pos]
        if '#' in before:
            break
        before = '.' * pos
        if match[2] != '':
            remainder = line[pos + n + 1:]
            after = '.'
        else:
            after = ''
            remainder = ''

        s = before + '#' * n + after

        results += [s + r for r in arrangements(remainder, groups[1:])]

    return results


def unfold(lines):
    for line, groups in lines:
        yield '?'.join([line]*5), groups * 5
