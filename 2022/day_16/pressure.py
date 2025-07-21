from functools import cache
from itertools import repeat, chain

import networkx as nx

from utils.aocd_solutions import Puzzle
from utils.bitmask import BitmaskSet
from utils.parser import groups

puzzle = Puzzle(2022, 16)


def create_relaxed_graph(data):
    pressures, edges = dict(), dict()
    for v, p, e in groups(data, r"Valve (..) .*=(\d+);.*valves? (.+)"):
        pressures[v] = int(p)
        edges[v] = e.split(', ')

    g = nx.Graph(edges)

    # We construct our relaxed weighted directed graph based on the time cost of travelling between
    # two vertices and opening the valve. We can prune valves with 0 pressure.
    # We assume 'AA', the start point, always has 0 pressure.
    gw = nx.DiGraph(
        {src: {t: {'weight': w + 1} for t, w in ts.items() if pressures[t] > 0 if t != src} for src, ts in
         nx.shortest_path_length(g) if src == 'AA' or pressures[src] > 0})

    # Add pressure data
    for n, p in pressures.items():
        if n in gw:
            gw.add_node(n, pressure=p)

    # For my puzzle input, gw has 16 nodes and 225 edges.
    return gw


class Search:

    def __init__(self, g, heuristic_time_step=None):
        self.g = g
        self.pressures = {n: self.g.nodes.data()[n]['pressure'] for n in self.g.nodes.keys()}
        self.time_step_iter = heuristic_time_step if heuristic_time_step else lambda t: range(t - 2, 0, -2)
        self.NodeSet = BitmaskSet(self.g['AA'].keys())

    initial_position = 'AA', 0

    @cache
    def get_edges(self, curr):
        return self.NodeSet(self.g[curr].keys())

    @cache
    def value_func(self, t_rem, curr, tgt):
        # The pressure*time total output from visiting a node and opening the valve
        dt = self.g[curr][tgt]['weight']
        t = max(0, t_rem - dt)
        return t * self.g.nodes.data()[tgt]['pressure'], dt

    @cache
    def upper_bound(self, unseen, time):
        # Gets the upper bound on the best value of a sub-problem
        # Assumes all edges for the whole graph are w=2 and quickly sums over all unseen
        pressures = sorted([self.pressures[n] for n in unseen], reverse=True)
        return sum(p * t for p, t in zip(pressures, self.time_step_iter(time)))

    @cache
    def best_first_search(self, curr, unseen, time):
        # DFS but it greedily picks the best option first (in terms of value gained / time cost)

        if not unseen or time < 2:
            return 0

        lower_bound = 0
        targets = sorted([(n, self.value_func(time, curr, n)) for n in unseen & self.get_edges(curr)],
                         key=lambda t: t[1][0] / t[1][1], reverse=True)
        for tgt, (val, dt) in targets:
            new_unseen = unseen / tgt
            if val + self.upper_bound(new_unseen, time - dt) <= lower_bound:
                continue
            result = val + self.best_first_search(tgt, new_unseen, time - dt)
            lower_bound = max(result, lower_bound)

        return lower_bound

    def dfs(self, curr, unseen, time):
        if not unseen or time < 2:
            yield 0, ~unseen
            return

        for tgt in unseen & self.get_edges(curr):
            val, dt = self.value_func(time, curr, tgt)
            new_unseen = unseen / tgt
            yield val, ~new_unseen
            yield from ((val + v, n) for v, n in self.dfs(tgt, new_unseen, time - dt))

    def __call__(self, total_time, num_agents=1):

        nodes = self.NodeSet.all()
        if num_agents == 1:
            return self.best_first_search('AA', nodes, total_time)
        elif num_agents == 2:

            paths = dict()
            for val, visited in self.dfs('AA', nodes, total_time):
                if visited in paths:
                    paths[visited] = max(paths[visited], val)
                else:
                    paths[visited] = val

            paths = sorted(paths.items(), key=lambda v: -v[1])

            best_val = 0
            for i, (v1, r1) in enumerate(paths):
                if r1 < paths[0][1] / 1.5:
                    break
                for v2, r2 in paths[i + 1:]:
                    if not v1 & v2:
                        if r1 + r2 <= best_val:
                            break
                        best_val = max(best_val, r1 + r2)

            return best_val


def time_step_heuristic(t):
    it = chain(repeat(4, 2), repeat(5, 1), repeat(10))
    t -= 2
    while t > 0:
        yield t
        t -= next(it)


@puzzle.solution_a
def solve_p1(data):
    g = create_relaxed_graph(data)
    result = Search(g, time_step_heuristic)(30, 1)
    return result


@puzzle.solution_b
def solve_p2(data):
    g = create_relaxed_graph(data)
    result = Search(g, time_step_heuristic)(26, 2)
    return result


puzzle.check_examples()
puzzle.check_solutions()
