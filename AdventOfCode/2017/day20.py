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

parts = read("example").split("\n\n")
if not read.from_example:
    parts.extend(parts)

particles_p1 = [Particle(*matcher(l)) for l in parts[0].splitlines()]
particles_p2 = [Particle(*matcher(l)) for l in parts[1].splitlines()]

# Part 1


def project(particle):
    return tuple(Particle(p, v, a) for p, v, a in zip(*particle))


def min_steps_to_align(particle: Particle):
    (p, v, a) = particle
    ticks = 0
    while p * a < 0 or p * v < 0:
        v += a
        p += v
        ticks += 1
    return ticks


def advance(particle, k):
    [px, py, pz] = [
        Particle(p.p + k * p.v + k * (k + 1) * p.a // 2, p.v + k * p.a, p.a)
        for p in project(particle)
    ]
    return Particle((px.p, py.p, pz.p), (px.v, py.v, pz.v), (px.a, py.a, pz.a))


def manhattan(point3d):
    return abs(point3d[0]) + abs(point3d[1]) + abs(point3d[2])


def slowest(particles: list[Particle]):
    # We need to first align the sign of the particles' positions & velocities with
    # the sign of their acceleration. For that, we compute the number of ticks that
    # are necessary to wait before the sign are aligned then we advance all the
    # particles by that number of ticks.
    ticks = max(
        min_steps_to_align(p) for particle in particles for p in project(particle)
    )
    adv = [advance(particle, ticks) for particle in particles]
    # Finally the slowest particles are those with smallest acceleration then velocity
    # then position (considering manhattan distance of all axis).
    m = min(
        range(len(adv)),
        key=lambda i: (manhattan(adv[i].a), manhattan(adv[i].v), manhattan(adv[i].p)),
    )
    return (m, particles[m])


part_one(slowest(particles_p1)[0])

# Part 2


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
    # constraints that solutions must be positive integer values only.

    a = particle_1.a - particle_2.a
    b = 2 * (particle_1.v - particle_2.v) + a
    c = 2 * (particle_1.p - particle_2.p)

    if a == 0 and b == 0 and c == 0:
        return ALL

    return set(s for s in solve_integer_quadratic_eq(a, b, c) if s >= 0)


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


part_two(len(particles_p2) - len(flatten(collisions(particles_p2).values())))
