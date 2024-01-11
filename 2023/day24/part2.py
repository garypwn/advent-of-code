from hailstones import *

hailstones = Hailstones(open("input.txt"))

# Check for any parallel hailstones for an easy solution
print(f"Parallel hailstones: {len(hailstones.find_parallel_hailstones())}")
