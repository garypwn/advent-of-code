from collections import deque

from utils import parser
from utils.aocd_solutions import Puzzle
from utils.grid_2d import DIRECTIONS
from utils.vector import Vector2

puzzle = Puzzle(2024, 18)


def parse(data):
    return {Vector2(x, y): t for t, (x, y) in enumerate(parser.integers(data))}


def bfs(pts, start=(0, 0), end=(70, 70), time=0):
    start, end = Vector2(start), Vector2(end)
    q = deque([Vector2(start)])
    visited = {start: None}  # {Pt: parent} dict

    while q:
        pt = q.popleft()
        for tgt in (pt + d for d in DIRECTIONS):
            if 0 <= tgt <= end and tgt not in visited:
                if tgt in pts and pts[tgt] < time:  # Wall check
                    continue

                q.append(tgt)
                visited[tgt] = pt
        if pt == end:
            break

    if end not in visited:
        return None

    valid_until = None
    path = []
    nxt = end
    while nxt is not None:
        if nxt in pts:
            valid_until = min(valid_until, pts[nxt]) if valid_until else pts[nxt]
        path.append(nxt)
        nxt = visited[nxt]

    path.reverse()
    return path, valid_until


@puzzle.solution_a
def solve_p1(data, end=(70, 70), start_time=1024):
    path, _ = bfs(parse(data), end=end, time=start_time)
    return len(path[1:])


@puzzle.solution_b
def solve_p2(data, end=(70, 70), start_time=1024):
    time = start_time
    pts = parse(data)
    while result := bfs(pts, end=end, time=time):
        path, until = result
        time = until + 1

    for pt, t in pts.items():
        if t == time - 1:
            return f"{pt[0]},{pt[1]}"


puzzle.check_examples((6, 6), 12)
puzzle.check_solutions()
