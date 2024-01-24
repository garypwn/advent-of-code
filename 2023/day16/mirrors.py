from functools import cache

from utils.idx_tools import UP, DOWN, RIGHT, LEFT, bounds, chararray
from utils.tuples import add


def energized(lights):
    return len(set((x for x, _ in lights)))


def entry_points(shape):
    ds = ((RIGHT, LEFT), (DOWN, UP))
    for s, (f, b) in zip(shape, ds):
        for i in range(s):
            yield (i, 0), f
            yield (i, s - 1), b


class Mirror:

    def __init__(self, lines):
        self.grid = chararray(lines)

    @cache
    def _propagate(self, light):

        idx, d = light
        match self.grid[idx]:
            case '.':
                ds = [d]
            case '/':
                ds = [(-d[1], -d[0])]
            case '\\':
                ds = [(d[1], d[0])]
            case '-':
                ds = {
                    RIGHT: [RIGHT],
                    LEFT: [LEFT],
                    UP: [RIGHT, LEFT],
                    DOWN: [RIGHT, LEFT]
                }[d]
            case '|':
                ds = {
                    UP: [UP],
                    DOWN: [DOWN],
                    LEFT: [UP, DOWN],
                    RIGHT: [UP, DOWN]
                }[d]
            case _:
                raise ValueError()

        new_lights = set()
        for d in ds:
            new_idx = add(idx, d)
            if bounds(self.grid, new_idx):
                new_lights.add((new_idx, d))

        return new_lights

    def process_light(self, pos=(0, 0), direction=RIGHT):
        lights = set()
        queue = {(pos, direction)}

        while queue:
            light = queue.pop()
            queue |= self._propagate(light) - lights
            lights.add(light)

        return lights
