import re
from typing import Iterable

from walk import Hiking


def new_map(lines: Iterable[str]):
    p = re.compile(r"[<>v^]")
    for line in lines:
        line = p.sub(".", line)
        yield line


m = Hiking(new_map(open("input.txt")))

print(f"There are {len(m.edge_list)} junctions.")  # 35
# As far as I can tell the problem is NP-Hard, but with only 35 junctions it should be brute-forceable.


