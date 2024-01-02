from typing import Iterable, Sequence


class Hiking:
    grid: list[list[str]]  # The input map
    start: tuple[int, int] = None
    end: tuple[int, int] = None
    width: int = None
    height: int = None
    edge_list: dict = None

    def __init__(self, lines: Iterable[str]):

        self.grid = []
        for line in lines:
            line = line.strip()
            if self.width:
                if len(line) != self.width:
                    raise ValueError("Length of lines must be constant.")
            else:
                self.width = len(line)

            self.grid.append([*line])

        self.height = len(self.grid)

        for i, char in enumerate(self.grid[0]):
            if char == ".":
                if self.start:
                    raise ValueError("Multiple entry points.")
                self.start = (0, i)

        for i, char in enumerate(self.grid[-1]):
            if char == ".":
                if self.end:
                    raise ValueError("Multiple exit points.")
                self.end = (self.width - 1, i)

        if not (self.start and self.end):
            raise ValueError("Must have start and end point.")

        self.build_graph()

    def __getitem__(self, keys):
        value = self.grid
        if not isinstance(keys, Iterable):
            return value[keys]
        for key in keys:
            value = value[key]

        return value

    def __setitem__(self, keys, value):
        if isinstance(keys, Sequence):
            target = self.grid
            for key in keys[:-1]:
                target = target[key]
            target[keys[-1]] = value

        else:
            self.grid[keys] = value

    def get_moves(self, pt: tuple[int, int], origin=None) -> list[tuple[int, int]]:
        # Checks what points can be moved to from this one
        moves = []
        directions = {(1, 0): 'v', (0, 1): '>', (-1, 0): '^', (0, -1): '<'}
        for direction, char in directions.items():
            target = tuple(p + d for p, d in zip(pt, direction))

            # If we are on a v>^< slope we must follow the slope
            if self[pt] in directions.values() and self[pt] != char:
                continue

            # Check map bounds. Shouldn't be a problem since the map is walled but just in case.
            if target[0] not in range(self.height) or target[1] not in range(self.width):
                continue

            # Check if we're about to move into an uphill slope
            if self[target] == directions[tuple(-x for x in direction)]:
                continue

            # Optional exclude origin
            if origin is not None and target == origin:
                continue

            if self[target] == '.' or self[target] in directions.values():
                moves.append(target)

        return moves

    def get_subpaths(self, pt: tuple[int, int]) -> dict[tuple[int, int]: int]:
        # Gets the next junctions reachable from a point, and the number of steps to each junction
        subpaths = []
        for curr in self.get_moves(pt):
            steps = 1
            last = pt
            while True:

                # Take a step
                moves = self.get_moves(curr, last)

                # Path leads back to the starting point
                if curr == pt:
                    print(f"Found a self-loop at {pt}")
                    break

                # Check if we are at the start or end
                if curr == self.end or curr == self.start:
                    subpaths.append((curr, steps))
                    break

                # Check for non-start or finish dead end
                if len(moves) < 1:
                    print(f"Found a dead end at {curr}")
                    break

                # Go until we hit a junction
                if len(moves) > 1:
                    subpaths.append((curr, steps))
                    break

                last = curr
                curr = moves[0]
                steps += 1

        return subpaths

    def build_graph(self):
        # Builds the junction graph
        self.edge_list = {}
        vertex_queue = [self.start]
        while vertex_queue:
            pt = vertex_queue.pop(0)
            if pt in self.edge_list.keys():
                continue
            self.edge_list[pt] = []

            paths: list = self.get_subpaths(pt)
            if len(paths) == 0:
                print(f"Found dead end junction at {pt}")

            for destination, weight in paths:
                if destination in self.edge_list.keys():
                    print(f"Found a cycle at {pt}")
                elif destination != self.start and destination != self.end:
                    vertex_queue.append(destination)
                self.edge_list[pt].append((destination, weight))

    def junctions(self):
        # Iterates over junctions, start, and end, in topological order

        junctions = set(self.edge_list.keys())
        stack = []

        def topological_sort_helper(node):
            junctions.remove(node)
            for child, _ in self.edge_list[node]:
                if child in junctions:
                    topological_sort_helper(child)
            stack.append(node)

        for junction in junctions.copy():
            if junction in junctions:
                topological_sort_helper(junction)

        return stack[::-1]

    def longest_path(self, start):
        # Finds the longest path from start to each reachable junction assuming the graph is a DAG.

        distances = {start: 0}  # Length from start to a given junction

        for current_v in self.junctions():

            # Skip things before start point is okay because of topological ordering
            if current_v not in distances:
                continue

            # Relax distance each outgoing edge
            for outgoing_v, weight in self.edge_list[current_v]:
                if outgoing_v not in distances:
                    distances[outgoing_v] = distances[current_v] + weight
                else:
                    distances[outgoing_v] = max(distances[outgoing_v], distances[current_v] + weight)

        return distances

