import networkx as nx

from utils.aocd_solutions import Puzzle
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
        {src: {t: {'weight': w} for t, w in ts.items() if pressures[t] > 0 if t != src} for src, ts in
         nx.shortest_path_length(g) if src == 'AA' or pressures[src] > 0})

    # Add pressure data
    for n, p in pressures.items():
        if n in gw:
            gw.add_node(n, pressure=p)

    # For my puzzle input, gw has 16 nodes and 225 edges.
    return gw


def exhaustive_search(g, total_time):
    # Maps 2^16 states to their respective pareto fronts, stored as dicts of {t_rem: value}
    # Each pareto front's size is at most t/2, since the min edge weight is 2 minutes, and all are integers.
    pareto_fronts = dict()

    def pareto_efficient(state, val, t):
        # Check and update pareto dict
        if state not in pareto_fronts:
            pareto_fronts[state] = {t: val}
            return True

        front = pareto_fronts[state]
        for i in range(total_time, t - 1, -1):
            if i in front:
                if val <= front[i]:
                    return False
        front[t] = val
        return True

    def dfs(state, val, t_rem):

        if t_rem <= 0:
            return val

        curr, seen = state

        def value_func(tgt):
            t = t_rem - g[curr][tgt]['weight']
            return t * g.nodes.data()[tgt]['pressure'], t

        best_val = val

        for dest in g[curr].keys() - seen:
            v, new_t = value_func(dest)
            new_val = val + v
            new_state = dest, seen - {curr}
            if pareto_efficient(new_state, new_val, new_t):
                best_val = max(best_val, dfs(new_state, new_val, new_t))

        return best_val

    return dfs(('AA', frozenset({'AA'})), 0, total_time)


@puzzle.solution_a
def solve_p1(data):
    g = create_relaxed_graph(data)
    return exhaustive_search(g, 30)


puzzle.check_examples()
