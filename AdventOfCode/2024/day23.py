from libs import *

# Parse input

connections = Graph.from_edges([tuple(l.split("-")) for l in read_lines("example")])

# Part 1


def three_cliques(g: Graph):
    cliques = set()
    for a, b in g.edges():
        for c in g.neighbors(a):
            if c != b and (a, c) in g and (b, c) in g:
                cliques.add(tuple(sorted([a, b, c])))
    return cliques


part_one(
    len([c for c in three_cliques(connections) if any(n.startswith("t") for n in c)])
)

# Part 2

part_two(sorted(connections.maximum_clique()), sep=",")
