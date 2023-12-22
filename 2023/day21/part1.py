from sys import stdin

from garden import Garden

g = Garden(open("input.txt"))

for _ in range(64):
    g = g.step()

print(g)
print(g.count_destinations())