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


print(predict([10, 13, 16, 21, 30, 45]))
