import re

import igraph

from utils.aocd_solutions import Puzzle
from utils.grid_2d import DIRECTIONS, CW, CCW, RIGHT
from utils.vector import Vector2

puzzle = Puzzle(2024, 16)


def parse(data):
    pts = set()
    start = None
    end = None
    for i, line in enumerate(data.split('\n')):
        for j, c in enumerate(line):
            pt = Vector2(i, j)
            match c:
                case '.':
                    pts.add(pt)
                case 'S':
                    start = pt
                    pts.add(pt)
                case 'E':
                    end = pt
                    pts.add(pt)

    return pts, start, end


def name(pt, d):
    return str(pt.pt + (d,))


def make_graph(pts, end) -> igraph.Graph:
    edges = []
    for pt in pts:
        for d in DIRECTIONS:
            # We represent points as (x, y, d) tuples
            p = name(pt, d)

            if pt + d in pts:
                edges.append((p, name(pt + d, d), 1))

            for d_t in (CW[d], CCW[d]):
                edges.append((p, name(pt, d_t), 1000))

            if pt == end:
                edges.append((p, 'end', 0))

    return igraph.Graph.TupleList(edges, directed=True, weights=True)


@puzzle.solution_a
def solve_p1(data):
    pts, start, end = parse(data)
    graph = make_graph(pts, end)
    distances = graph.distances(source=name(start, RIGHT), target='end', weights="weight")
    return int(min(distances[0]))


@puzzle.solution_b
def solve_p2(data):
    pts, start, end = parse(data)
    graph = make_graph(pts, end)
    paths = graph.get_all_shortest_paths(name(start, RIGHT), to='end', weights="weight")

    # Very dumb solution parsing points from vertices which have string names
    pts_in_path = set()
    pattern = re.compile(r"\((\d+), (\d+)")
    for path in paths:
        for pt in path:
            s = graph.vs[pt]['name']
            if s == 'end':
                continue
            pts_in_path.add(tuple(pattern.search(s).groups()))

    return len(pts_in_path)


puzzle.check_examples()
puzzle.check_solutions()
