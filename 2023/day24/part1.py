from hailstones import *

hailstones = Hailstones(open("input.txt"))

intersections = hailstones.find_intersections()
# print(intersections)
# print()
print(f"Found {len(intersections)} intersections.")
