from collections import deque
from copy import deepcopy

# Parse file

connections = {
    l.split(": ")[0]: l.split(": ")[1].split()
    for l in open("AdventOfCode/2023/examples/day25.in").read().strip().split("\n")
}


# Part 1


def mirror_connections(graph):
    vertices = set(graph.keys()) | set(sum(graph.values(), []))
    mirror = {e: set() for e in vertices}
    for e, it in graph.items():
        mirror[e] = mirror[e] | set(it)
        for i in it:
            mirror[i].add(e)
    return mirror


def groups(graph):
    vertices = set(graph.keys())
    groups = []
    while vertices:
        e = vertices.pop()
        visited = {e}
        next = {e}
        while next:
            n = next.pop()
            for neigh in graph[n]:
                if neigh not in visited:
                    vertices.remove(neigh)
                    visited.add(neigh)
                    next.add(neigh)
        groups.append(visited)
    return groups


def rem(graph, edges):
    g2 = deepcopy(graph)
    for n1, n2 in edges:
        g2[n1].remove(n2)
        g2[n2].remove(n1)
    for d in [n for n in g2 if len(g2[n]) == 0]:
        del g2[d]
    return g2


def cut_edges(starts, targets, graph):
    edges = []
    for s in starts:
        edges += [(s, e) for e in graph[s] if e in targets]
    return edges


def cut(graph, excl):
    out = set()
    g = graph
    while len(out) == 0 or (
        len(g.keys()) > 0 and len(cut_edges(g.keys(), out, graph)) > 3
    ):
        priorities = sorted(list(g.keys()), key=lambda n: len(g[n]))
        priority = 0
        n = priorities[priority]
        while len(out) == 0 and n in excl:
            priority += 1
            n = priorities[priority]
        if len(out) == 0:
            excl.append(n)
        out.add(n)
        g = rem(g, [(o1, n) for o1 in g[n]])

    # Check answer & compute group sizes
    grs = groups(rem(graph, cut_edges(g.keys(), out, graph)))
    if len(grs) == 2:
        return len(grs[0]) * len(grs[1])

    # If answer is incorrect, try another one (starting from another point)
    return cut(graph, excl)


print("Part 1:", cut(mirror_connections(connections), []))
