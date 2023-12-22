# From the solution to part 1, we can see that when traversing the infinite garden, the first point the elf
# will enter a new cell is ALWAYS the cardinal or inter-cardinal points. To reach a new cell, he will have to take
# 131 steps in a cardinal direction. From the center cell, he will have to take 66 steps. So we get something like:

#                         590
#                     525 459 525
#                 525 394 328 394 525
#             525 394 263 197 263 394 525
#         525 459 263 132  66 132 263 459 525
#     590 459 328 197  66   0  66 197 328 459 590
#         525 459 263 132  66 132 263 459 525
#             525 394 263 197 263 394 525
#                 525 394 328 394 525
#                     525 459 525
#                         590

# So, while the center cross is a special exception where the elf enters by a cardinal, all other cells the elf
# enters by a corner, and the number of steps he's taken is
# S = 1 + 131*(x-1) where x is the manhattan distance of the cell from the center.

# So, if we want to figure out the terminal manhattan distance of the elf after S steps, we just solve for S:
# x = (S-1) / 131 + 1

from garden import Garden

g = Garden(open("input.txt"))

odd_even_test = g.__copy__()
for _ in range(200):
    odd_even_test = odd_even_test.step()

print(f"Even garden: {(even_count := odd_even_test.count_destinations())}")
odd_even_test = odd_even_test.step()
print(f"Odd garden: {(odd_count := odd_even_test.count_destinations())}")


# Even garden: 7325
# Odd garden: 7265
# Sadly this means we need to track evens and odds.


# Now we figure out how  many complete cells there are after the elf finishes all his steps
elf_steps = 26501365
complete_cell_radius = (elf_steps - 66) // 131 + 1
print(f"\nThe elf can complete {complete_cell_radius} cells in a straight line.")
odd_cells, even_cells = (complete_cell_radius - 1) ** 2, complete_cell_radius ** 2
print(f"The number of odd/even completed cells are: {odd_cells, even_cells}")

# Now we have a subtotal for our number of steps, not including cells at the edge:
print(f"Size from completed cells: {(total := odd_count * odd_cells + even_count * even_cells)}")

# Now we figure out our middle edge steps
remaining_steps_at_middle = (elf_steps - 66) % 131
print(f"Edge cells: {remaining_steps_at_middle} steps remain.")

for p in [(g.size() // 2, 0), (g.size() - 1, g.size() // 2), (0, g.size() // 2), (g.size() // 2, g.size() - 1)]:
    edge = g.move_start(*p)
    for _ in range(remaining_steps_at_middle):
        edge = edge.step()

    d = edge.count_destinations()
    print(f"Edge has {d} plots")
    total += d

# Now we figure out corners
remaining_steps_at_corner = (elf_steps - 132) % 131
print(f"Corner cells: {remaining_steps_at_corner} steps remain.")

for p in [(0, 0), (0, g.size() - 1), (g.size() - 1, 0), (g.size() - 1, g.size() - 1)]:
    corner = g.move_start(*p)

    # Start with outside corners
    for _ in range(remaining_steps_at_corner):
        corner = corner.step()
    d = corner.count_destinations()

    # From our earlier pattern formula, we know that the number of corner cells is n-1
    total += d * complete_cell_radius
    print(f"Outer corner has {d} plots")

    # Move to inside corners
    for _ in range(131):
        corner = corner.step()
    d = corner.count_destinations()

    total += d * (complete_cell_radius - 1)
    print(f"Inner corner has {d} plots.")


print(f"Total plots: {total}")
