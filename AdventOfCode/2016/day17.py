from libs import *

# Parse input

passcode = read("example")

directions = "UDLR"
UDLR = {d: Point.UDLR[n] for d, n in zip(directions, "^v<>")}

# Part 1


def accessible_rooms(path):
    return (
        d
        for d, h in zip(directions, md5((passcode + path).encode()).hexdigest()[:4])
        if h in "bcdef"
    )


class VaultAStar(AStar):
    def neighbors(self, node):
        p, path = node
        if p == Point(3, 3):
            # cannot go past the vault
            return
        for d in accessible_rooms(path):
            if (p + UDLR[d]).is_within_bounds(4, 4):
                yield (p + UDLR[d], path + d)

    def is_goal_reached(self, current, goal=None):
        return current[0] == goal


vault_shortest_path = VaultAStar()

part_one(vault_shortest_path.solve((Point.ZERO, ""), Point(3, 3)).goal.node[1])

# Part 2


def longest_path(starting_points, goal):
    step = 0
    path = ""
    while starting_points:
        step += 1
        reachable = set()
        for p in starting_points:
            for p2 in vault_shortest_path.neighbors(p):
                reachable.add(p2)
                if p2[0] == goal and len(p2[1]) > len(path):
                    path = p2[1]
        starting_points = reachable
    return path


part_two(len(longest_path({(Point.ZERO, "")}, Point(3, 3))))
