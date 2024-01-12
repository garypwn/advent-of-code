import numpy as np

from hailstones import *

hailstones = Hailstones(open("input.txt"), dtype=np.double)

# Check for any parallel hailstones for an easy solution
# print(f"Parallel hailstones: {len(hailstones.find_parallel_hailstones())}")


# We only care about 3 hailstones for this solution, so we'll just arbitrarily pick the first 3
hailstones.stones = hailstones.stones[0:5]


def compute_plane(stone_i, stone_j):
    p_i, v_i = stone_i
    p_j, v_j = stone_j

    d = (p_i - p_j) @ np.cross(v_i, v_j)
    n = np.cross((p_i - p_j), (v_i - v_j))

    return n, d


# Get our n and d values
planes = []
for i, j in ((0, 1), (1, 2), (2, 0)):
    planes.append(compute_plane(hailstones.stones[i], hailstones.stones[j]))

N = np.array([n for n, _ in planes])
D = np.array([d for _, d in planes])

# Solve for velocity
v = np.linalg.solve(N, D)
print(f"\nVelocity: {v}")  # Sanity check to see if they're all integers

# Apply velocity adjustment to hailstones array
for i, stone in enumerate(hailstones.stones):
    hailstones.stones[i, 1] -= v

intersections = hailstones.find_intersections(False)
position = np.mean(intersections, 0)

# Sanity check: see if the intersections are all the same and also integers
print()
print("Intersections:")
print("\n".join(str(x) for x in intersections))
print()
print(f"Starting position (median): ", *(f"{x:.2f}, " for x in position))
