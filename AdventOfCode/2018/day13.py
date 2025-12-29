from libs import *
from typing import ClassVar

# Parse input

track1 = read("example")
track1, track2 = track1.split("\n\n") if read.from_example else (track1, track1)

track1 = track1.splitlines()[1 if read.from_example else 0 :]
track2 = track2.splitlines()[1 if read.from_example else 0 :]


# Part 1


@dataclass(frozen=True)
class Cart:
    position: Point
    direction: str
    turn_state: int = 0

    ROTATIONS: ClassVar = {
        (">", "-"): ">",
        (">", "/"): "^",
        (">", "\\"): "v",
        ("<", "-"): "<",
        ("<", "/"): "v",
        ("<", "\\"): "^",
        ("v", "|"): "v",
        ("v", "/"): "<",
        ("v", "\\"): ">",
        ("^", "|"): "^",
        ("^", "/"): ">",
        ("^", "\\"): "<",
    }

    TURNS: ClassVar = [-90, 0, 90]

    def __lt__(self, other: Cart):
        self = (self.position.y, self.position.x, self.direction, self.turn_state)
        other = (other.position.y, other.position.x, other.direction, other.turn_state)
        return self < other

    def turn(self):
        next_direction = Point.UDLR[self.direction].rotate(Cart.TURNS[self.turn_state])
        return next(d for d, p in Point.UDLR.items() if p == next_direction)

    def advance(self, tracks: Grid):
        next_pos = self.position + Point.UDLR[self.direction]
        if tracks[next_pos] == "+":
            next_dir = self.turn()
            next_turn = (self.turn_state + 1) % len(Cart.TURNS)
        else:
            next_dir = Cart.ROTATIONS[(self.direction, tracks[next_pos])]
            next_turn = self.turn_state
        return Cart(next_pos, next_dir, next_turn)


def parse_carts_and_tracks(unprocessed_tracks):
    tracks = Grid([list(r) for r in unprocessed_tracks])
    carts = [Cart(pos, d) for d in Point.UDLR for pos in tracks.find_all(d)]

    for c in carts:
        tracks[c.position] = "|" if Point.UDLR[c.direction].x == 0 else "-"

    return tracks, carts


def first_crash(unprocessed_tracks):
    tracks, carts = parse_carts_and_tracks(unprocessed_tracks)
    carts_by_position = {c.position: c for c in carts}
    while True:
        for c in sorted(carts_by_position.values()):
            del carts_by_position[c.position]
            c0 = c.advance(tracks)
            if c0.position in carts_by_position:
                return c0.position
            carts_by_position[c0.position] = c0


part_one(first_crash(track1).coordinates(), sep=",")

# Part 2


def last_cart(unprocessed_tracks):
    tracks, carts = parse_carts_and_tracks(unprocessed_tracks)
    carts_by_position = {c.position: c for c in carts}
    while len(carts_by_position) > 1:
        for c in sorted(carts_by_position.values()):
            if c.position not in carts_by_position:
                continue
            del carts_by_position[c.position]
            c0 = c.advance(tracks)
            if c0.position in carts_by_position:
                del carts_by_position[c0.position]
            else:
                carts_by_position[c0.position] = c0
    return next(iter(carts_by_position.values()))


part_two(last_cart(track2).position.coordinates(), sep=",")
