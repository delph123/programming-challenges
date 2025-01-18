from libs import *

# Parse file

connections_graph = Graph.undirected(
    {l.split(": ")[0]: set(l.split(": ")[1].split()) for l in read_lines("i")}
)


# Part 1


def edges_between(starts, targets, graph):
    edges = []
    for s in starts:
        edges += [(s, e) for e in graph[s] if e in targets]
    return edges


def cut(graph: Graph, excl):
    out = set()
    g = graph
    while len(out) == 0 or (len(g) > 0 and len(edges_between(g, out, graph)) > 3):
        priorities = sorted(g.nodes(), key=lambda n: len(g[n]))
        priority = 0
        n = priorities[priority]
        while len(out) == 0 and n in excl:
            priority += 1
            n = priorities[priority]
        if len(out) == 0:
            excl.append(n)
        out.add(n)
        g = g.with_removed([(o1, n) for o1 in g[n]])

    # Check answer & compute group sizes
    grs = graph.with_removed(edges_between(g, out, graph)).groups()
    if len(grs) == 2:
        return len(grs[0]) * len(grs[1])

    # If answer is incorrect, try another one (starting from another point)
    return cut(graph, excl)


part_one(cut(connections_graph, []))
