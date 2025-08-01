import networkx as nx

from utils import tuples
from utils.aocd_solutions import Puzzle
from utils.parser import integers

puzzle = Puzzle(2022, 18)

DIRECTIONS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
DIRECTIONS = DIRECTIONS + tuple(tuples.neg(d) for d in DIRECTIONS)


def adjacent_cubes(cube):
    for d in DIRECTIONS:
        yield tuples.add(cube, d)


def exposed_surfaces(cubes, direction=False):
    # Faces are (cube, cube) pairs.
    # Directional faces face 'out' of the mass of cubes i.e. face[0] is in cubes and face[1] is not.
    directional_faces = set()
    faces = dict()
    for cube in cubes:
        for directional_face in ((cube, c) for c in adjacent_cubes(cube)):
            face = frozenset(directional_face)
            if direction:
                directional_faces.add(directional_face)
            if face in faces:
                faces[face] += 1
            else:
                faces[face] = 1
    if direction:
        return {df for df in directional_faces if faces[frozenset(df)] == 1}
    return {k for k, v in faces.items() if v == 1}


def adjacent_faces(face, faces):
    c1, c2 = face
    norm = tuples.sub(c2, c1)

    for d in DIRECTIONS:
        if d == norm or d == tuples.neg(norm):
            continue

        # Adjacent faces in the plane
        f0 = tuples.add(c1, d), tuples.add(c2, d)
        # Perpendicular to the plane
        f90 = tuples.add(c2, d), c2  # Rotate up
        f270 = c1, tuples.add(c1, d)  # Rotate down

        # Make sure to yield only one of these since diagonal movement isn't allowed
        if f90 in faces:
            yield f90
        elif f270 in faces:
            yield f270
        elif f0 in faces:
            yield f0


def make_graph(faces):
    g = nx.Graph()
    g.add_nodes_from(faces)
    for face in faces:
        g.add_edges_from(((face, f) for f in adjacent_faces(face, faces)))
    return g


@puzzle.solution_a
def solve_p1(data):
    cubes = list(tuple(c) for c in integers(data))
    return len(exposed_surfaces(cubes))


@puzzle.solution_b
def solve_p2(data):
    cubes = list(tuple(c) for c in integers(data))
    faces = exposed_surfaces(cubes, direction=True)
    g = make_graph(faces)
    surfaces = list(nx.connected_components(g))

    # We assume the largest surface is the 'outside,' though that may not be true for some degenerate inputs
    return max(len(s) for s in surfaces)

puzzle.check_examples()
puzzle.check_solutions()
