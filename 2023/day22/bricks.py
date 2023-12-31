from __future__ import annotations

from typing import Iterable


class Brick:
    # Represents a brick

    ends: list[list[int, int, int], tuple[int, int, int]]  # Ends of the brick in x,y,z order
    supported: bool  # Set if there is ground, or a tower of bricks touching the ground, below this brick.
    supporting: list[Brick]
    supporters: list[Brick]

    def __init__(self, p1: list[int, int, int], p2: list[int, int, int]):
        self.ends = [p1, p2]
        self.supporting = []
        self.supporters = []
        self.supported = self.on_ground()

    def on_ground(self):
        return True if self.ends[0][2] == 1 or self.ends[1][2] == 1 else False

    def top_height(self):
        return max(self.ends[0][2], self.ends[1][2])

    def bottom_height(self):
        return min(self.ends[0][2], self.ends[1][2])

    def contains(self, pt: tuple[int, int, int]):
        # Check is a point is inside the brick, including at an end point.
        for i, c in enumerate(zip(*self.ends)):
            x = pt[i]
            if x > c[0] and x > c[1]:
                return False
            if x < c[0] and x < c[1]:
                return False

        return True

    def supports_point(self, pt: tuple[int, int, int]):
        # Check if a point is supported by the brick
        if not self.supported:
            return False

        return self.contains((pt[0], pt[1], pt[2] - 1))

    def supports_brick(self, brick: Brick):
        # Check if this brick supports another brick.
        for pt in brick.bottom_face():
            if self.supports_point(pt):
                return True
        return False

    def bottom_face(self):
        return self.__iter__(bottom_face=True)

    def safely_disintegratable(self):
        for brick in self.supporting:
            if len(brick.supporters) <= 1:
                return False

        return True

    def __iter__(self, bottom_face=False):
        # Iterates over the points in the brick
        def p_range(p1, p2):
            return range(p1, p2 + 1) if p1 <= p2 else (p2, p1 + 1)

        if bottom_face:
            z = min(self.ends[0][2], self.ends[1][2])
            for x in p_range(self.ends[0][0], self.ends[1][0]):
                for y in p_range(self.ends[0][1], self.ends[1][1]):
                    yield x, y, z

        for x in p_range(self.ends[0][0], self.ends[1][0]):
            for y in p_range(self.ends[0][1], self.ends[1][1]):
                for z in p_range(self.ends[0][2], self.ends[1][2]):
                    yield x, y, z


class FallingBricks:
    bricks: list[Brick]
    unsupported_bricks: list[Brick]
    supported_bricks: list[Brick]

    def __init__(self, lines: Iterable[str] | None):
        self.bricks = []
        self.unsupported_bricks = []
        self.supported_bricks = []

        if lines is not None:
            for line in lines:
                strings = line.split('~')
                pts = [string.split(',') for string in strings]
                self.add_brick(Brick(*[[int(s) for s in pt] for pt in pts]))

    def add_brick(self, brick: Brick):
        if brick.supported:
            self.supported_bricks.append(brick)
        else:
            self.unsupported_bricks.append(brick)
        self.bricks.append(brick)

    def step(self):
        # Moves all the bricks down one z-level, checking for collisions.

        # Bricks get sorted by z-level of their bottom face, so lower bricks should resolve first
        self.unsupported_bricks.sort(key=lambda b: b.bottom_height())

        # Supported bricks get sorted by z-level of their top face
        self.supported_bricks.sort(key=lambda b: b.top_height())

        for brick in self.unsupported_bricks[:]:

            z = brick.bottom_height()

            # Check if on ground
            if brick.on_ground():
                brick.supported = True
                self.unsupported_bricks.remove(brick)
                self.supported_bricks.append(brick)
                continue

            # Check if supported by another brick
            for i, supported_brick in enumerate(self.supported_bricks[:]):

                # We can ignore bricks whose tops are on the wrong z-level
                if supported_brick.top_height() != z - 1:
                    continue

                # And by maintaining a sorted list we can terminate early
                if supported_brick.top_height() > z:
                    break

                if supported_brick.supports_brick(brick):
                    if not brick.supported:
                        brick.supported = True
                        self.unsupported_bricks.remove(brick)
                        self.supported_bricks.insert(i, brick)

                    supported_brick.supporting.append(brick)
                    brick.supporters.append(supported_brick)

            # Move the brick down one if it still isn't supported
            if not brick.supported:
                for end in brick.ends:
                    end[2] -= 1

    def settle_bricks(self):
        print(f"Dropping {len(self.bricks)} bricks.")
        counter = 1
        while self.unsupported_bricks:
            print(f"    Step {counter: 4}   {len(self.unsupported_bricks): 5} unsupported bricks remain.")
            counter += 1
            self.step()
        print(f"All bricks are supported after {counter} steps.\n")

    def disintegratable_bricks(self):
        return filter(lambda brick: brick.safely_disintegratable(), self.bricks)
