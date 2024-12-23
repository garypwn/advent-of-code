from igraph import Graph

from utils import parser
from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2024, 23)


def make_graph(data):
    edges = [tuple(line) for line in parser.find_in_line(data, r"\w+")]
    return Graph.TupleList(edges)


@puzzle.solution_a
def solve_p1(data):
    g = make_graph(data)
    ct = 0
    for clique in g.cliques(3, 3):
        if any(g.vs[i]['name'][0] == 't' for i in clique):
            ct += 1
    return ct


@puzzle.solution_b
def solve_p2(data):
    g = make_graph(data)
    clique = g.largest_cliques()[0]
    names = [g.vs[i]['name'] for i in clique]
    names.sort()
    return ','.join(names)


puzzle.check_solutions()
