from libs import *

# Parse input

racetrack = read_grid("example")

min_savings = 0 if read.from_example else 100
min_savings_p2 = 50 if read.from_example else 100

start = racetrack.index("S")
end = racetrack.index("E")

# Part 1


class TrackAStar(AStar):
    def neighbors(self, node: Point):
        return (
            node + d for d in Point.UDLR.values() if racetrack.get(node + d, "#") != "#"
        )


def cheats_2sec():
    shortest_path = {
        p: i for (i, p) in enumerate(TrackAStar().solve(start, end).path())
    }
    cheat_coordinates = {}
    for p, i in shortest_path.items():
        for d1, d2 in product(Point.UDLR.values(), repeat=2):
            if shortest_path.get(p + d1 + d2, 0) > i + 2:
                cheat_coordinates[(p, p + d1 + d2)] = (
                    shortest_path.get(p + d1 + d2, 0) - i - 2
                )
    return cheat_coordinates


part_one(
    len([(cheat, win) for (cheat, win) in cheats_2sec().items() if win >= min_savings])
)

# Part 2


def cheats_from_position(sp, start: Point, dist: int):
    x0 = max(start.x - dist, 0)
    x1 = min(start.x + dist + 1, len(racetrack.rows()[0]))
    y0 = max(start.y - dist, 0)
    y1 = min(start.y + dist + 1, len(racetrack.rows()))
    cheats_by_savings = defaultdict(int)
    for x in range(x0, x1):
        for y in range(y0, y1):
            p = Point(x, y)
            if start.manhattan(p) > dist:
                continue
            win = sp.get(p, 0) - sp[start] - start.manhattan(p)
            if win > 0:
                cheats_by_savings[win] += 1
    return cheats_by_savings


def cheats(duration):
    shortest_path = {
        p: i for (i, p) in enumerate(TrackAStar().solve(start, end).path())
    }
    cheats_by_savings = defaultdict(int)
    for p in shortest_path.keys():
        for win, nb_cheats in cheats_from_position(shortest_path, p, duration).items():
            cheats_by_savings[win] += nb_cheats
    return cheats_by_savings


part_two(sum([cheats for (win, cheats) in cheats(20).items() if win >= min_savings_p2]))
