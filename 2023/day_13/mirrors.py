import itertools

import numpy as np


def parse(lines):
    arr = []
    for line in lines:

        if line == '\n':
            yield np.array(arr)
            arr = []
            continue

        arr.append([s == '#' for s in line.strip()])

    if arr:
        yield np.array(arr)


def find_reflection(arr: np.array, exclude):
    # Finds the horizontal line of reflection

    for i in range(1, len(arr)):
        end = min(2 * i, len(arr))
        start = 2 * i - end
        if (arr[start:i] == arr[i:end][::-1]).all():
            if not ((0 < exclude < 100) and i == exclude):
                return i


def summarize(arr, exclude=0):
    if r := find_reflection(arr, exclude // 100):
        return r * 100

    if r := find_reflection(np.moveaxis(arr, 1, 0), exclude):
        return r


def de_smudge(arr):
    # Destructive to arr

    old_summary = summarize(arr)

    prev = None
    for pt in itertools.product(range(len(arr)), range(len(arr[0]))):
        if prev:
            arr[prev] = not arr[prev]

        arr[pt] = not arr[pt]
        prev = pt

        r = summarize(arr, old_summary)
        if r is not None:
            return r

    raise ValueError()
