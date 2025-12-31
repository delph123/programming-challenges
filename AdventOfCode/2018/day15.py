from libs import *
from dataclasses import field

# Parse input

battle_ground = read_grid("example")

GOBLIN = "G"
ELF = "E"


# Part 1


class ShortestPath(AStar):
    def __init__(self, battle_ground):
        super().__init__(visit_closed=True)
        self.battle_ground = battle_ground

    def neighbors(self, n):
        return [n + p for p in Point.UDLR.values() if self.battle_ground[n + p] == "."]


@dataclass
class Unit:
    shortest_path: ShortestPath = field(repr=False)
    position: Point
    kind: str
    attack_power: int = 3
    hit_points: int = 200

    def __lt__(self, other: Unit):
        return (self.position.y, self.position.x) < (other.position.y, other.position.x)

    def is_dead(self):
        return self.hit_points <= 0

    def find_attack_target(self, enemies: Units):
        e = enemies.find_all(
            enemies.filter(position=[self.position + p for p in Point.UDLR.values()])
        )
        if len(e) == 0:
            return None
        return min(e, key=lambda u: (u.hit_points, u.position.y, u.position.x))

    def distance(self, p: Point):
        solution = self.shortest_path.solve(self.position, p)
        if solution is None:
            return None
        next_move = min(solution.nodes_by_distance()[1], key=lambda p: (p.y, p.x))
        return (solution.cost(), p.y, p.x, next_move)

    def move(self, battle_ground: Grid, enemies: Units):
        move_target = set(
            e.position + p
            for e in enemies
            for p in Point.UDLR.values()
            if battle_ground[e.position + p] == "."
        )

        if len(move_target) == 0:
            return None

        try:
            d, _, _, n = min(filter(None, (self.distance(p) for p in move_target)))
        except ValueError:
            return None

        battle_ground[self.position] = "."
        battle_ground[n] = self.kind
        self.position = n

        if d == 1:
            return self.find_attack_target(enemies)
        else:
            return None

    def take_damage(self, hp: int, battle_ground: Grid):
        self.hit_points -= hp
        # Remove from the map if it is dead
        if self.is_dead():
            battle_ground[self.position] = "."

    def turn(self, battle_ground: Grid, enemies: Units):
        if self.is_dead() or len(enemies) == 0:
            return
        e = self.find_attack_target(enemies)
        if not e:
            e = self.move(battle_ground, enemies)
        if e:
            e.take_damage(self.attack_power, battle_ground)


@dataclass
class Units:
    units: list[Unit]

    def __iter__(self):
        return iter(sorted(u for u in self.units if not u.is_dead()))

    def __len__(self):
        return len(self.units)

    def filter(self, *, position=None, kind=None):
        return (
            lambda u: (position is None or u.position in position)
            and (kind is None or u.kind == kind)
            and not u.is_dead()
        )

    def find_all(self, f):
        return Units(list(filter(f, self.units)))

    def by_kind(self, kind):
        return self.find_all(self.filter(kind=kind))


def combat_outcome(battle_ground: Grid, attack_power=3):
    sp = ShortestPath(battle_ground)
    goblins = [Unit(sp, p, "G", 3) for p in battle_ground.find_all(GOBLIN)]
    elves = [Unit(sp, p, "E", attack_power) for p in battle_ground.find_all(ELF)]
    units = Units(goblins + elves)
    completed = False
    round = 0
    while not completed:
        round += 1
        for u in units:
            enemies = units.by_kind(GOBLIN if u.kind == ELF else ELF)
            if len(enemies) == 0:
                completed = True
                break
            u.turn(battle_ground, enemies)
            if attack_power > 3 and u.kind == ELF and u.is_dead():
                completed = True
                break

    # print(
    #     f"After {round} rounds with attack power {attack_power}: {len(units.by_kind(ELF))} elves survived."
    # )

    if attack_power == 3 or len(units.by_kind(ELF)) == len(elves):
        return (round - 1) * sum(u.hit_points for u in units)
    else:
        return 0


part_one(combat_outcome(battle_ground.copy()))

# Part 2


def min_attack_power(battle_ground):
    @cache
    def outcome(ap):
        return combat_outcome(battle_ground.copy(), ap)

    i = bisect(range(4, 201), True, key=lambda ap: outcome(ap) > 0, smallest=True)
    return outcome(range(4, 201)[i])


part_two(min_attack_power(battle_ground))
