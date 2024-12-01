import re

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2024, 1)

def parse(data):
    lists = [], []
    pattern = re.compile(r"(\d+)\s+(\d+)")
    for line in data.split('\n'):
        for l, g in zip(lists, pattern.match(line).groups()):
            l.append(int(g))

    return lists

@puzzle.solution_a
def sum_distances(data):
    l1, l2 = parse(data)
    l1.sort()
    l2.sort()

    return sum([abs(a - b) for a, b in zip(l1, l2)])

@puzzle.solution_b
def similarity_score(data):
    l1, l2 = parse(data)
    counts = {n: 0 for n in l1}
    for i in l2:
        if i in counts:
            counts[i] += 1
        else:
            counts[i] = 1

    return sum(counts[i] * i for i in l1)

puzzle.check_examples()
puzzle.check_solutions()