from collections.abc import Iterable

import igraph as ig


def read_input(lines: Iterable[str]):
    edges = {}
    for line in lines:
        node, vertices = line.split(':')
        node = node.strip()
        vertices = [v.strip() for v in vertices.split()]
        edges[node] = vertices

    return edges


def create_graph(edges: dict):
    graph = ig.Graph()

    # Check nodes list and targets for all vertices, add to graph
    graph.add_vertices(list(set(edges.keys()) | {t for ts in edges.values() for t in ts}))
    graph.add_edges([(v, t) for v in edges.keys() for t in edges[v]])
    return graph

