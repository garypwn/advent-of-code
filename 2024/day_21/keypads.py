from functools import cache

from utils.aocd_solutions import Puzzle
from utils.grid_2d import UP, LEFT
from utils.vector import Vector2

puzzle = Puzzle(2024, 21)

MAIN_KEYPAD = [
    '789',
    '456',
    '123',
    ' 0A'
]

ROBOT_KEYPAD = [
    ' UA',
    'LDR'
]


class Keypad:

    def pos(self, value):
        if isinstance(value, str):
            return self.keypad[value]
        else:
            return value

    def __hash__(self):
        return hash(repr(self.keypad))

    def __eq__(self, other):
        return other.keypad == self.keypad

    def __init__(self, keypad):
        self.keypad = {}
        for i, line in enumerate(keypad):
            for j, c in enumerate(line):
                if c is not None and c != ' ':
                    self.keypad[c] = Vector2(i, j)
                if c == 'A':
                    self._pos = Vector2(i, j)

        reverse = {}
        for k, v in self.keypad.items():
            reverse[v] = k

        self.keypad |= reverse

    def path_to(self, pos, tgt):
        if isinstance(tgt, str):
            tgt = self.keypad[tgt]

        return tgt - self.pos(pos)

    def seq_to(self, pos, tgt):
        pos = self.pos(pos)
        y, x = self.path_to(pos, tgt)

        if x == 0 and y == 0:
            yield 'A'
            return

        if (dy := y // UP[0]) > 0:
            s_y = 'U' * dy
        elif dy < 0:
            s_y = 'D' * -dy
        else:
            s_y = ''
        corner_v = pos + (y, 0)

        if (dx := x // LEFT[1]) > 0:
            s_x = 'L' * dx
        elif dx < 0:
            s_x = 'R' * -dx
        else:
            s_x = ''
        corner_h = pos + (0, x)

        if x != 0 and corner_h in self.keypad:
            yield s_x + s_y + 'A'
        if y != 0 and corner_v in self.keypad:
            yield s_y + s_x + 'A'

@cache
def chain_keypads(keypads, seq: str):
    if not keypads:
        return len(seq)

    keypad = keypads[0]
    pos = 'A'

    ct = 0
    for s in seq:
        results = (chain_keypads(keypads[1:], new_seq) for new_seq in keypad.seq_to(pos, s))
        pos = s
        ct += min(results)

    return ct


@puzzle.solution_a
def solve_p1(data, intermediate_robots=2):
    keypads = (Keypad(MAIN_KEYPAD),) + (Keypad(ROBOT_KEYPAD),) * intermediate_robots
    complexities = []
    for line in data.split('\n'):
        complexities.append(int(line[0:3]) * chain_keypads(keypads, line))

    return sum(complexities)

@puzzle.solution_b
def solve_p2(data):
    return solve_p1(data, 25)


puzzle.check_solutions()
