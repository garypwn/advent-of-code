import re
from typing import Iterable

from walk import Hiking


def new_map(lines: Iterable[str]):
    p = re.compile(r"[<>v^]")
    for line in lines:
        line = p.sub(".", line)
        yield line


m = Hiking(new_map(open("input.txt")))


def junction_count():
    print(f"There are {len(m.edge_list)} junctions.")  # 35

    # As far as I can tell the problem is NP-Hard, but with only 35 junctions it could be brute-forceable.
    # Assuming each junction has 4 outgoing edges (many have less) that gives us O(4^35) which is like a sextillion...
    # But I'm sure it will be fine


def plot_graph():
    import igraph
    import matplotlib.pyplot
    import matplotlib.pyplot as plt

    vertices = list(m.edge_list.keys())
    if m.start not in vertices:
        vertices.append(m.start)
    if m.end not in vertices:
        vertices.append(m.end)

    edges = []
    idx_map = {}

    for i, v in enumerate(vertices):
        idx_map[v] = i

    for i, v in enumerate(vertices):
        if v in m.edge_list:
            for u, weight in m.edge_list[v]:
                edges.append((i, idx_map[u], weight))

    g = igraph.Graph(len(vertices), [(v, u) for v, u, _ in edges], directed=True)
    g.es["weight"] = [w for _, _, w in edges]
    g.vs["name"] = vertices

    fig, ax = matplotlib.pyplot.subplots(figsize=(20, 12))
    igraph.plot(
        g.as_undirected(mode="each", combine_edges=max),
        target=ax,
        layout="auto",
        autocurve=False,
        vertex_size=65,
        vertex_color=["salmon" if pt == m.start or pt == m.end else "steelblue" for pt in g.vs["name"]],
        vertex_label=[f"{y},{x}" for y, x in g.vs["name"]],
        edge_color="gray",
        edge_width=2,
        edge_label=g.es["weight"],
        edge_label_size=9,
        edge_label_dist=0
    )

    plt.show()


longest_path, distance = m.longest_path(m.start, m.end)
print(f"\nLongest path: {distance} steps.")


