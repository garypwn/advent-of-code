from __future__ import annotations

import bisect
import re
import string
from typing import Iterable


class Range:
    # A sorted range

    sub_ranges: list[tuple] or None

    def __init__(self, start=None, length=None):
        if start is None:
            self.sub_ranges = []
        else:
            self.sub_ranges = [(start, length)]

        self.length = None

    def __getitem__(self, item):

        if isinstance(item, slice):
            r = Range()
            stop = min(item.stop, len(self)) if item.stop else len(self)
            idx_start = item.start if item.start else 0
            if idx_start >= len(self):
                return r

            curr = 0
            for start, length in self.sub_ranges:
                if curr <= idx_start < curr + length:
                    if curr + length >= stop:
                        # Edge case for if the entire slice is within this subrange
                        r.sub_ranges.append((idx_start - curr + start, stop - idx_start))
                        break

                    else:
                        # First sub range
                        r.sub_ranges.append((idx_start - curr + start, length - idx_start + curr))

                elif idx_start <= curr < stop:
                    if curr + length > stop:
                        # Final sub range
                        r.sub_ranges.append((start, stop - curr))

                    else:
                        # Middle ranges
                        r.sub_ranges.append((start, length))
                else:
                    break

                curr += length

            return r

        rem = item
        for start, length in self.sub_ranges:
            if length > rem:
                return start + rem

            rem -= length

        raise IndexError()

    def __add__(self, other: Range or int):
        # No overlapping ranges pls
        r = Range()

        if isinstance(other, int):
            r.sub_ranges = [(start + other, length) for start, length in self.sub_ranges]
            return r

        if not self.sub_ranges:
            r.sub_ranges = other.sub_ranges[:]
            return r
        if not other.sub_ranges:
            r.sub_ranges = self.sub_ranges[:]
            return r

        r.sub_ranges = self.sub_ranges[:]
        for sub in other.sub_ranges:
            bisect.insort(r.sub_ranges, sub, key=lambda s: s[0])

        return r

    def __contains__(self, item):
        for start, length in self.sub_ranges:
            if start <= item < start + length:
                return True

        return False

    def __len__(self):
        if not self.length:
            self.length = sum(length for _, length in self.sub_ranges)
        return self.length

    def sub_range_iter(self):
        for start, length in self.sub_ranges:
            yield Range(start, length)

    def last(self):
        start, length = self.sub_ranges[-1]
        return start + length - 1


class SeedMap:

    def __init__(self, lines: Iterable[str]):
        self.mappings = {}
        for line in lines:
            dest, source, length = (int(s) for s in line.split())
            self.mappings[source] = (dest, length)

        self.lookup = sorted(self.mappings.keys())

    def _get_range_helper(self, r):
        # r is a contiguous range

        if len(r) == 0:
            return Range()

        idx = bisect.bisect(self.lookup, r[0])

        if idx == 0:
            source = 0
            dest = 0
            length = self.lookup[0]
        else:
            source = self.lookup[idx - 1]
            dest, length = self.mappings[source]

        r_start, r_length = r.sub_ranges[0]

        if source <= r_start < source + length:
            # r is in a mapping range

            diff = r_start - source
            mapped = r[:length - diff]
            mapped += dest - source
            remainder = r[length - diff:]

        else:
            if idx >= len(self.lookup):
                return r[:]
            source = self.lookup[idx]
            diff = source - r_start
            mapped = r[:diff]
            remainder = r[diff:]

        return mapped + self._get_range_helper(remainder)

    def __getitem__(self, item):

        if isinstance(item, Range):
            r = Range()
            for sub in item.sub_range_iter():
                r += self._get_range_helper(sub)
            return r

        idx = bisect.bisect(self.lookup, item)
        if idx == 0:
            return item

        source = self.lookup[idx - 1]
        dest, length = self.mappings[source]

        if not (source <= item < source + length):
            return item

        return dest - source + item


def read_input(lines: Iterable[str], seed_ranges=False):
    iterator = lines.__iter__()
    seeds = [int(s) for s in re.findall(r"\b\d+\b", next(iterator))]
    if seed_ranges:
        seeds = [Range(source, length) for source, length in zip(seeds[::2], seeds[1::2])]

    def iterate():
        for s in lines:
            if not s[0] in string.digits:
                break
            yield s

    mappings = []
    for line in lines:
        if line.strip() == "":
            continue

        name = line.strip("\n:")
        mappings.append(SeedMap(iterate()))

    return seeds, mappings
