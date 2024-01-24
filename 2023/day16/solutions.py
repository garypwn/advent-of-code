from mirrors import *

m = Mirror(open('input.txt'))
print(f"Part 1: Number of energized tiles: {energized(m.process_light())}")
print(f"Part 2: Maximum energized tiles: {max((energized(m.process_light(*p)) for p in entry_points(m.grid.shape)))}")