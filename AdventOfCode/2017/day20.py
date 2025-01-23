from libs import *
from collections import namedtuple

Particle = namedtuple("Particle", "p v a")

ALL = [-1]

# Parse input
matcher = create_matcher(
    [
        (
            "p=<{int},{int},{int}>, v=<{int},{int},{int}>, a=<{int},{int},{int}>",
            ((0, 1, 2), (3, 4, 5), (6, 7, 8)),
        )
    ]
)

particles = [Particle(*matcher(l)) for l in read_lines("i")]

# Part 1


def manhattan(point3d):
    return abs(point3d[0]) + abs(point3d[1]) + abs(point3d[2])


def slowest(particles: list[Particle]):
    # TODO normalize particles
    return sorted(
        enumerate(particles),
        key=lambda p: (manhattan(p[1].a), manhattan(p[1].v), manhattan(p[1].p)),
    )[0]


part_one(slowest(particles)[0])

# Part 2


def solve_integer_quadratic_eq(a, b, c):
    # Solve a quadratic equation with coefficients and solutions all
    # being integer values.
    #
    #   delta = b^2 - 4ac
    #   s = ( -b ± sqrt(delta) ) / 2a
    #
    # To collide, following conditions must hold true:
    #   delta >= 0
    #   s is an integer

    if a == 0:
        if b == 0 and c == 0:
            # everything match, send a special value
            return ALL
        elif b == 0:
            return []
        if c % b == 0 and -c // b > 0:
            return [-c // b]
        else:
            return []

    delta = b**2 - 4 * a * c

    if delta == 0 and b % (2 * a) == 0:
        return [-b // (2 * a)]

    if delta <= 0 or int(sqrt(delta)) ** 2 != delta:
        return []

    sqrt_delta = int(sqrt(delta))
    solutions = []
    if (b + sqrt_delta) % (2 * a) == 0:
        solutions.append((-b - sqrt_delta) // (2 * a))
    if (b - sqrt_delta) % (2 * a) == 0:
        solutions.append((-b + sqrt_delta) // (2 * a))
    return []


def collide1d(particle_1, particle_2):
    # The general formula for the position of a particle after k ticks is:
    #   position((p,v,a), k) = p + k * v + k * (k + 1) * a / 2
    #
    # Hence, two particles collide when:
    #   position((p1,v1,a1), k) - position((p2,v2,a2), k) == 0
    # or:
    #   2 * (p1 - p2) + k * ( 2 * (v1 - v2) + (a1 - a2) ) + k^2 * (a1 - a2) == 0
    # for some value of k.
    #
    # Solving for k, we have:
    #   a = (p1 - p2)
    #   b = 2 * (v1 - v2) + (a1 - a2)
    #   c = (a1 - a2)
    #
    # And we can compute the solutions of a quadratic equation with the additional
    # constraints that solutions must be integer values only.

    a = particle_1.a - particle_2.a
    b = 2 * (particle_1.v - particle_2.v) + a
    c = 2 * (particle_1.p - particle_2.p)

    return set(s for s in solve_integer_quadratic_eq(a, b, c) if s >= 0)


def project(particle):
    return tuple(Particle(p, v, a) for p, v, a in zip(*particle))


def collide(particle_1, particle_2):
    # Compute k for each x,y,z coordinate separately
    k_coords = [
        collide1d(p1, p2) for (p1, p2) in zip(project(particle_1), project(particle_2))
    ]
    # Merge all k and find the min
    k = reduce(lambda u, v: v if u == ALL else (u if v == ALL else v & u), k_coords)
    if k == ALL:
        return 0
    elif len(k) >= 1:
        return min(k)


def collisions(particles):
    # Generate all pairs of particles colliding
    pairs = []
    for p1, p2 in product(range(len(particles)), repeat=2):
        if p1 > p2:
            l = collide(particles[p1], particles[p2])
            if l is not None:
                pairs.append((l, (p1, p2)))
    # Enumerate all collisions
    parts = {}
    while pairs:
        m = min(l for l, _ in pairs)
        parts[m] = set(x for l, pair in pairs for x in pair if l == m)
        pairs = [(l, (a, b)) for (l, (a, b)) in pairs if len({a, b} & parts[m]) == 0]
    return parts


part_two(len(particles) - len(flatten(collisions(particles).values())))
