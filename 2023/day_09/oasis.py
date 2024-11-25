import itertools


def parse(lines):
    for line in lines:
        yield [int(s) for s in line.split()]


def deltas(nums):
    return [b - a for a, b in itertools.pairwise(nums)]


def predict(seq):
    if seq == [0 for _ in seq]:
        return 0

    return seq[-1] + predict(deltas(seq))


def predict_left(seq):
    if seq == [0 for _ in seq]:
        return 0

    return seq[0] - predict_left(deltas(seq))
