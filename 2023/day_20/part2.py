import math

import igraph as ig
import matplotlib.pyplot as plt
from modules import *

b = create_state_machine()


def plot_graph():
    vertices = [k for k in modules.keys()]
    edges = []
    for i, mod in enumerate(modules.values()):
        edges += [(i, next(v for v, name in enumerate(vertices) if name == s)) for s in mod.subscribers]

    g = ig.Graph(len(modules), edges, directed=True)
    g.vs["name"] = vertices
    for v in g.vs:
        match type(modules[v["name"]]).__name__:
            case "Conjunction":
                v["color"] = "salmon"
            case "FlipFlop":
                v["color"] = "steelblue"
            case "Dummy":
                v["color"] = "gold"
            case _:
                v["color"] = "grey"
    fig, ax = plt.subplots(figsize=(10, 10))
    ig.plot(
        g,
        target=ax,
        layout="graphopt",
        vertex_size=30,
        vertex_color=g.vs["color"],
        vertex_frame_width=0.5,
        vertex_frame_color="black",
        vertex_label=g.vs["name"],
        vertex_label_size=7.0,
        edge_width=1,
        edge_color="#AAA",
        edge_arrow_size=6,
        edge_arrow_width=6
    )

    plt.show()


plot_graph()

# From this graph we can see that only 4 conjunction modules feed into rx.
# Each of these modules has its own subgraph controlling it.
# All of these modules need to output high for rx to output low.
# If my intuition is correct, they will loop with predictable patterns.
targets = ['kp', 'tx', 'vg', 'gc']
history = {t: [] for t in targets}
for i in range(1, 100000):
    press_button(b)
    for t in targets:
        c = modules[t].counter[Signal.HIGH]
        if c == 1:
            history[t].append(i)
        if c > 1:
            print(f"{t} outputted {c} high signals on button press {i}")
        modules[t].reset_counter()


def pattern_check(seq):
    for x in seq:
        if x % seq[0] != 0:
            return False
    return True


for t, h in history.items():
    if pattern_check(h):
        print(f"{t} repeats every {h[0]} button presses.")
    else:
        print(f"{t} does not repeat.")

# If all 4 modules repeat regularly, then we can find the lcm of their repetition periods.
periods = (h[0] for h in history.values())
print(f"Result: {math.lcm(*periods)}")
