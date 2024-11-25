import re


def holiday_hash(s):
    x = 0
    for c in s:
        x += ord(c)
        x *= 17
        x %= 256
    return x


class HolidayMap:

    def __init__(self):
        self.boxes = {i: {} for i in range(256)}

    def __setitem__(self, key, value):
        self.boxes[holiday_hash(key)][key] = value

    def __getitem__(self, key):
        return self.boxes[holiday_hash(key)][key]

    def __contains__(self, key):
        return key in self.boxes[holiday_hash(key)]

    def __delitem__(self, key):
        if key not in self:
            return
        del self.boxes[holiday_hash(key)][key]

    def powers(self):
        for box, lenses in self.boxes.items():
            for i, lens in enumerate(lenses.values()):
                yield (1 + box) * (1 + i) * lens


def initialization(line):
    boxes = HolidayMap()
    for match in re.finditer(r"(\w+)(=|-)(\d*)", line):
        label, op, value = match.groups()
        if op == '=':
            boxes[label] = int(value)
        elif op == '-':
            del boxes[label]
        else:
            raise ValueError()

    return boxes
