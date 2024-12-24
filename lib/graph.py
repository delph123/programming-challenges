from collections import defaultdict


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

    def bron_kerbosch(self, clique: set, candidates: set, excluded: set):
        if not candidates and not excluded:
            yield clique
        while candidates:
            c = candidates.pop()
            nc = self.neighbor(c, set())
            for cq in self.bron_kerbosch(
                clique | set([c]), candidates & nc, excluded & nc
            ):
                yield cq
            excluded.add(c)

    def cliques(self):
        return list(self.bron_kerbosch(set(), self.nodes(), set()))

    def maximum_clique(self):
        return max(self.bron_kerbosch(set(), self.nodes(), set()), key=len)