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

        if (dy := y // UP[0]) > 0:
            s_y = 'U' * dy
        elif dy < 0:
            s_y = 'D' * -dy
        else:
            s_y = ''
        v_corner = pos + (y, 0)

        if (dx := x // LEFT[1]) > 0:
            s_x = 'L' * dx
        elif dx < 0:
            s_x = 'R' * -dx
        else:
            s_x = ''
        h_corner = pos + (0, x)

        if dy != 0 and v_corner in self.keypad:
            yield s_y + s_x + 'A'
        if dx != 0 and h_corner in self.keypad:
            yield s_x + s_y + 'A'


def chain_keypads(keypads, seq: str, states: tuple):
    if not keypads:
        yield seq, states
        return

    keypad = keypads[0]
    pos = states[0]

    for s in seq:
        for s2 in keypad.seq_to(pos, s):
            results = list(chain_keypads(keypads[1:], s2, states[1:]))
            results.sort(key=lambda r: len(r[0]))
            result, new_states = results[0]
            pos = s
            states = (pos,) + new_states
            yield result, states


@puzzle.solution_a
def solve_p1(data):
    keypads = [Keypad(MAIN_KEYPAD)] + [Keypad(ROBOT_KEYPAD)] * 3
    for line in data.split('\n'):
        return ''.join(s for s, _ in chain_keypads(keypads, line, ('A',) * 4))


rrr = solve_p1("""029A
980A
179A
456A
379A""")
print(rrr)
