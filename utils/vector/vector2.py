import math


class Vector2:

    def __init__(self, *argv):
        if not argv:
            self.pt = (0, 0)
        elif len(argv) == 1:
            self.pt = tuple(argv[0])
        else:
            self.pt = tuple(argv)

        if len(self.pt) != 2:
            raise ValueError

    def __repr__(self):
        return repr(self.pt)

    def __getitem__(self, item):
        return self.pt[item]

    def __iter__(self):
        return iter(self.pt)

    def __len__(self):
        return 2

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self[0] + other, self[1] + other)
        else:
            return Vector2(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self[0] - other, self[1] - other)
        else:
            return Vector2(self[0] - other[0], self[1] - other[1])

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self[0] * other, self[1] * other)
        else:
            return Vector2(self[0] * other[0], self[1] * other[1])

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self[0] / other, self[1] / other)
        else:
            return Vector2(self[0] / other[0], self[1] / other[1])

    def __floordiv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self[0] // other, self[1] // other)
        else:
            return Vector2(self[0] // other[0], self[1] // other[1])

    def __floor__(self):
        return Vector2(math.floor(self[0]), math.floor(self[1]))

    def __and__(self, other):
        if hasattr(other, '__getitem__') and len(other) == 2:
            return Vector2(self[0] and other[0], self[1] and other[1])
        return bool(self) and other

    def __or__(self, other):
        if hasattr(other, '__getitem__') and len(other) == 2:
            return Vector2(self[0] or other[0], self[1] or other[1])
        return bool(self) or other

    def __bool__(self):
        return all(self.pt)

    def __eq__(self, other):
        if self[0] == other[0] and self[1] == other[1]:
            return True

    def __hash__(self):
        return hash(self.pt)

    def __neg__(self):
        return Vector2(-self[0], -self[1])

    def __lt__(self, other):
        if hasattr(other, '__getitem__') and len(other) == 2:
            return Vector2(self[0] < other[0], self[1] < other[1])
        return Vector2(self[0] < other, self[1] < other)

    def __gt__(self, other):
        if hasattr(other, '__getitem__') and len(other) == 2:
            return Vector2(self[0] > other[0], self[1] > other[1])
        return Vector2(self[0] > other, self[1] > other)

    def __ge__(self, other):
        if hasattr(other, '__getitem__') and len(other) == 2:
            return Vector2(self[0] >= other[0], self[1] >= other[1])
        return Vector2(self[0] >= other, self[1] >= other)

    def __le__(self, other):
        if hasattr(other, '__getitem__') and len(other) == 2:
            return Vector2(self[0] <= other[0], self[1] <= other[1])
        return Vector2(self[0] <= other, self[1] <= other)

    def dot(self, other):
        return self[0] * other[0] + self[1] * other[1]

    def length_squared(self):
        return self[0] ** 2 + self[1] ** 2

    def length(self):
        return math.sqrt(self.length_squared())

    def normalized(self):
        if self.pt == (0, 0):
            return Vector2()
        return self / self.length()
