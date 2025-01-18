from functools import partial


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


class Graph:

    def __init__(self, edges, oriented=False):
        self.neighbors = {}
        for a, b in edges:
            self.neighbors.setdefault(a, set())
            self.neighbors.setdefault(b, set())
            self.neighbors[a].add(b)
            if not oriented:
                self.neighbors[b].add(a)

    def neighbor(self, n, default=None):
        return self.neighbors.get(n, default)

    def __len__(self):
        return len(self.neighbors)

    def __contains__(self, e):
        if isinstance(e, tuple):
            (a, b) = e
            return a in self.neighbors and b in self.neighbors[a]
        else:
            e in self.neighbors

    def __getitem__(self, n):
        return self.neighbor[n]

    def nodes(self):
        return set(self.neighbors.keys())

    def edges(self):
        for start, nb in self.neighbors.items():
            for end in nb:
                yield (start, end)

    def _pivoted(self, candidates, excluded):
        if candidates:
            return candidates - max(
                (candidates & self.neighbor(c) for c in (candidates | excluded)),
                key=len,
            )
        else:
            return candidates

    def _bron_kerbosch(self, clique: set, candidates: set, excluded: set):
        if not candidates and not excluded:
            yield clique
        for c in self._pivoted(candidates, excluded):
            nc = self.neighbor(c, set())
            yield from self._bron_kerbosch(clique | {c}, candidates & nc, excluded & nc)
            candidates.remove(c)
            excluded.add(c)

    def cliques(self):
        return list(self._bron_kerbosch(set(), self.nodes(), set()))

    def maximum_clique(self):
        return max(self._bron_kerbosch(set(), self.nodes(), set()), key=len)

    def accessible_from(self, start):
        return adjacent(start, self.neighbor)

    def groups(self):
        return list(group_adjacent(self.nodes(), self.neighbor))
