from graph import *

g = create_graph(read_input(open("input.txt")))
cut = g.mincut()

print(f"Found minimum cut with weight {cut.value}")
print(f"Cluster 0 size: {cut.size(0)}")
print(f"Cluster 1 size: {cut.size(1)}")
