from utils import *


def parse(lines):
    return np.char.asarray([[s for s in line.strip()] for line in lines], itemsize=1)


class Mirror:

    def __init__(self, lines):
        self.grid = parse(lines)
        self.lights = set()

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
            if bounds(new_idx, self.grid):
                new_lights.add((new_idx, d))

        return new_lights

    def process(self, pos=(0, 0), direction=RIGHT):
        queue = {(pos, direction)}

        while queue:
            light = queue.pop()
            queue |= self._propagate(light) - self.lights
            self.lights.add(light)

    def energized(self):
        return len(set((x for x, _ in self.lights)))

