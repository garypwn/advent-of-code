import cProfile

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2024, 19)


def parse(data):
    tokens, patterns = data.split('\n\n')
    return tokens.split(', '), patterns.split('\n')


def match(pattern, tokens, known=None):
    if known is None:
        known = dict()

    if len(pattern) in known:
        return known[len(pattern)]

    ct = 0
    for token in tokens:

        # Short circuit if we know the pattern is dead
        if -1 in known:
            return 0

        if pattern == token:
            ct += 1
        elif pattern[:len(token)] == token:
            ct += match(pattern[len(token):], tokens, known)

    known[len(pattern)] = ct

    for i in range(1, len(tokens[0]) + 1):
        if i not in known or known[i] > 0:
            break
    else:
        known[-1] = 0  # We use index -1 to mark if the entire pattern is dead

    return ct


@puzzle.solution_a
def solve_p1(data):
    tokens, patterns = parse(data)
    tokens = sorted(tokens, key=len, reverse=True)
    return sum(1 if match(pattern, tokens) > 0 else 0 for pattern in patterns)


@puzzle.solution_b
def solve_p2(data):
    tokens, patterns = parse(data)
    tokens = sorted(tokens, key=len, reverse=True)
    return sum(match(pattern, tokens) for pattern in patterns)


puzzle.check_examples()
puzzle.check_solutions()
