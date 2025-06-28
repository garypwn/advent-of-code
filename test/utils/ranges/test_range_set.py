from itertools import chain
from random import randint
from unittest import TestCase

from utils.ranges import RangeSet


class TestRangeSet(TestCase):
    def test_1000_random_ranges(self):
        for _ in range(1000):
            nums = RangeSet()
            ranges = []
            for _ in range(20):
                x = randint(-100, 100)
                r = (x, x + randint(1, 20))
                ranges.append(r)
                nums.add(r)

            set_ranges = set(chain(*(range(start, stop) for start, stop in ranges)))
            set_nums = set(nums)
            self.assertSetEqual(set_nums, set_ranges)
            self.assertEqual(len(nums), len(set_ranges))

            # print(f"{len(set_ranges)} integers blobbed into {len(nums.intervals)} intervals.")