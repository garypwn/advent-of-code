import re
from functools import cmp_to_key

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2024, 5)


class CmpTable:
    def __init__(self, data):
        pattern = re.compile(r"(\d+)\|(\d+)")
        self.table = dict()

        # Add direct rules to the table
        for line in data.split('\n'):
            p1, p2 = [int(s) for s in pattern.match(line).groups()]
            if p1 not in self.table:
                self.table[p1] = {p2}
            else:
                self.table[p1].add(p2)

    def _cmp(self, p1, p2):
        # Tells us if we can say for sure that p1 comes before p2

        # Pages without rules have to go at the end
        if p1 not in self.table:
            return False

        # Direct rules
        if p2 in self.table[p1]:
            return True

    def __call__(self, p1, p2):
        before, after = self._cmp(p1, p2), self._cmp(p2, p1)
        if before and not after:
            return -1
        elif after and not before:
            return 1

        raise ValueError()


def middle_page(pages: list):
    return pages[len(pages) // 2]


def parse(data):
    data1, data2 = data.split('\n\n')
    table = CmpTable(data1)
    lists = [[int(p) for p in line.split(',')] for line in data2.split('\n')]
    return table, lists

@puzzle.solution_a
def solve_p1(data):
    table, lists = parse(data)
    filtered = filter(lambda l: l == sorted(l, key=cmp_to_key(table)), lists)
    return sum((middle_page(l) for l in filtered))

@puzzle.solution_b
def solve_p2(data):
    table, lists = parse(data)
    ordered = [sorted(l, key=cmp_to_key(table)) for l in lists]
    filtered = []
    for i, l in enumerate(ordered):
        if lists[i] != l:
            filtered.append(l)

    return sum((middle_page(l) for l in filtered))



puzzle.check_examples()
puzzle.check_solutions()
