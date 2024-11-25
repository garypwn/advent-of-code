import itertools

import numpy as np


def parse(lines):
    return np.char.asarray([[s for s in line.strip()] for line in lines], itemsize=1)


_transposes = {  # (axis, step direction)
    'N': (1, 1),
    'S': (1, -1),
    'E': (0, -1),
    'W': (0, 1)
}


def roll(platform: np.array, direction):
    axis, step = _transposes[direction]
    arr = np.moveaxis(platform, axis, 0)[:, ::step]

    # Moves all the rocks as far left as they can go
    for row in arr:
        blocks = [-1] + list(np.where(row == '#')[0]) + [len(row)]
        for i1, i2 in itertools.pairwise(blocks):
            if i1 >= i2:
                continue
            n = sum(row[i1 + 1:i2] == 'O')
            if n == 0:
                continue
            row[i1 + 1:i2] = ['O'] * n + ['.'] * (len(row[i1 + 1:i2]) - n)


def spin(platform):
    for d in 'NWSE':
        roll(platform, d)


def predict(platform, count):
    hashes_seq = [hash(platform.tobytes())]
    hashes = set(hashes_seq)

    i = 0
    while True:
        i += 1
        spin(platform)
        s = hash(platform.tobytes())
        if s in hashes:
            break

        hashes.add(s)
        hashes_seq.append(s)

    offset = hashes_seq.index(s)
    target = (count - offset) % (i - offset)
    target = hashes_seq[target + offset]

    while True:
        if hash(platform.tobytes()) == target:
            return

        spin(platform)


def load(platform):
    return sum([(i + 1) * sum(row == 'O') for i, row in enumerate(platform[::-1])])
