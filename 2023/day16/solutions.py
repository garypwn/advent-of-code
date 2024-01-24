from mirrors import *

m = Mirror(open('input.txt'))
m.process()
print(f"Part 1: Number of energized tiles: {m.energized()}")
