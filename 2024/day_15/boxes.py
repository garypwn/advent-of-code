from utils.aocd_solutions import Puzzle
from utils.grid_2d import DIRECTION_DICT, RIGHT, LEFT, DOWN, UP
from utils.vector import Vector2

puzzle = Puzzle(2024, 15)


def parse(data, fat=False):
    grid, moves = data.split('\n\n')

    walls = set()
    boxes = set()
    start = None

    grid = grid.split('\n')
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            tgt = Vector2(i, j * (2 if fat else 1))
            match grid[i][j]:
                case '#':
                    walls.add(tgt)
                    if fat:
                        walls.add(tgt + RIGHT)
                case 'O':
                    boxes.add(tgt)
                case '@':
                    start = tgt

    return Grid(walls, boxes, start, fat), ''.join(moves.split('\n'))


class Grid:
    walls: set[Vector2]
    boxes: set[Vector2]
    pos: Vector2
    fat: bool

    def __init__(self, walls, boxes, start, fat=False):
        self.walls = walls
        self.boxes = boxes
        self.pos = start
        self.fat = fat

    def move(self, d):
        pos = self.pos
        if self.fat:
            # We actually need to check if a box is moveable before trying to move it in this case
            if self._moveable_fat(pos, d):
                self._move_obj_fat(pos, d)
        else:
            self._move_obj(pos, d)

    def _move_obj(self, p, d):
        # Return True if the move was successful

        if p in self.walls:
            return False

        tgt = p + d

        if p == self.pos:
            if self._move_obj(tgt, d):
                self.pos = tgt
                return True
        elif p in self.boxes:
            if self._move_obj(tgt, d):
                self.boxes.remove(p)
                self.boxes.add(tgt)
                return True
        else:
            # Empty space
            return True

        return False

    def _moveable_fat(self, p, d):
        # Returns true if the object can be moved
        if p in self.walls:
            return False

        tgt = p + d

        if p == self.pos:
            if self._moveable_fat(tgt, d):
                return True
        elif p in self.boxes:
            # We are in the left half of a box
            if d in (UP, DOWN):
                return self._moveable_fat(tgt, d) and self._moveable_fat(tgt + RIGHT, d)
            else:
                return self._moveable_fat(tgt, d)
        elif p + LEFT in self.boxes:
            # We are in the right half of a box
            if d in (UP, DOWN):
                return self._moveable_fat(tgt, d) and self._moveable_fat(tgt + LEFT, d)
            else:
                return self._moveable_fat(tgt, d)
        else:
            # Empty space
            return True

        return False

    def _move_obj_fat(self, p, d):
        # Returns true if the object can be moved
        tgt = p + d

        if p == self.pos:
            self._move_obj_fat(tgt, d)
            self.pos = tgt
        elif p in self.boxes:
            # We are in the left half of a box
            if d in (UP, DOWN):
                self._move_obj_fat(tgt, d)
                self._move_obj_fat(tgt + RIGHT, d)
            else:
                self._move_obj_fat(tgt, d)

            self.boxes.remove(p)
            self.boxes.add(tgt)
        elif p + LEFT in self.boxes:
            # We are in the right half of a box
            if d in (UP, DOWN):
                self._move_obj_fat(tgt, d)
                self._move_obj_fat(tgt + LEFT, d)
                self.boxes.remove(p + LEFT)
                self.boxes.add(tgt + LEFT)
            else:
                self._move_obj_fat(tgt, d)


def gps(p):
    # "The GPS coordinate of a box is equal to 100 times its distance from the top edge of the map
    # plus its distance from the left edge of the map."

    return 100 * p[0] + p[1]


@puzzle.solution_a
def solve_p1(data, fat=False):
    grid, moves = parse(data, fat)

    for d in (DIRECTION_DICT[m] for m in moves):
        grid.move(d)

    return sum(gps(box) for box in grid.boxes)


@puzzle.solution_b
def solve_p2(data):
    return solve_p1(data, True)


puzzle.check_examples()
puzzle.check_solutions()
