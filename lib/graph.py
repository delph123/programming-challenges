from typing import TypeVar, Generic
from copy import deepcopy


def adjacent(start, neighbors):
    visited = set()
    frontier = {start}
    while frontier:
        visited |= frontier
        frontier = set(e for f in frontier for e in neighbors(f)) - visited
    return visited


def group_adjacent(iterable, neighbors):
    visited = set()
    for e in iterable:
        if e not in visited:
            group = adjacent(e, neighbors)
            yield group
            visited |= group


def group_by_distance(neighbors, start):
    nodes = []
    visited = set()
    frontier = {start}
    while frontier:
        nodes.append(frontier)
        visited |= frontier
        frontier = set(e for f in frontier for e in neighbors(f) if e not in visited)
    return nodes


V = TypeVar("V")


class Graph(Generic[V]):

    def __init__(self, neighbors_map: dict[V, set[V]]):
        super().__init__()
        self.neighbors_map = neighbors_map

    @classmethod
    def undirected(cls, neighbors_map: dict[V, set[V]]):
        g = cls(deepcopy(neighbors_map))
        for start, nb in neighbors_map.items():
            for end in nb:
                g.neighbors_map.setdefault(end, set()).add(start)
        return g

    @classmethod
    def from_edges(cls, edges, oriented=False):
        neighbors_map = {}
        for a, b in edges:
            neighbors_map.setdefault(a, set())
            neighbors_map.setdefault(b, set())
            neighbors_map[a].add(b)
            if not oriented:
                neighbors_map[b].add(a)
        return cls(neighbors_map)

    def __len__(self):
        return len(self.neighbors_map)

    def neighbors(self, n, default=None):
        return self.neighbors_map.get(n, default)

    def __contains__(self, e):
        if isinstance(e, tuple):
            (a, b) = e
            return a in self.neighbors_map and b in self.neighbors_map[a]
        else:
            e in self.neighbors_map

    def __getitem__(self, n):
        return self.neighbors_map[n]

    def nodes(self):
        return set(self.neighbors_map.keys())

    vertices = nodes

    def edges(self):
        for start, nb in self.neighbors_map.items():
            for end in nb:
                yield (start, end)

    def __iter__(self):
        return iter(self.neighbors_map)

    def copy(self):
        return Graph(deepcopy(self.neighbors_map))

    def _pivoted(self, candidates, excluded):
        if candidates:
            return candidates - max(
                (candidates & self.neighbors(c) for c in (candidates | excluded)),
                key=len,
            )
        else:
            return candidates

    def _bron_kerbosch(self, clique: set, candidates: set, excluded: set):
        if not candidates and not excluded:
            yield clique
        for c in self._pivoted(candidates, excluded):
            nc = self.neighbors(c, set())
            yield from self._bron_kerbosch(clique | {c}, candidates & nc, excluded & nc)
            candidates.remove(c)
            excluded.add(c)

    def cliques(self):
        return list(self._bron_kerbosch(set(), self.nodes(), set()))

    def maximum_clique(self):
        return max(self._bron_kerbosch(set(), self.nodes(), set()), key=len)

    def accessible_from(self, start):
        return adjacent(start, self.neighbors)

    def groups(self):
        return list(group_adjacent(self, self.neighbors))

    def nodes_by_distance(self, start):
        return group_by_distance(self.neighbors, start)

    def with_removed(self, edges, oriented=False):
        g2 = self.copy()
        for n1, n2 in edges:
            g2[n1].remove(n2)
            if not oriented:
                g2[n2].remove(n1)
        for d in [v for v in g2 if len(g2[v]) == 0]:
            del g2.neighbors_map[d]
        return g2
