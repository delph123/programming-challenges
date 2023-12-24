from sympy import symbols, solve, Eq

# Parse file

hails = [
    (
        [int(n) for n in l.split(" @ ")[0].split(", ")],
        [int(n) for n in l.split(" @ ")[1].split(", ")],
    )
    for l in open("AdventOfCode/2023/examples/day24.in").read().strip().split("\n")
]

# Part 1


# Two hailstones collides in X,Y plane
#   with:
#     - hail 0 = px, py @ vx, vy
#     - hail 1 = qx, qy @ wx, wy
#   when:
#     - px + a * vx = qx + b * wx
#     - py + a * vy = qy + b * wy
#
#   therefore:
#     - a = (qx - px + b * wx) / vx
#     - b * wy = py - qy + vy * (qx - px + b * wx) / vx
#     - (wy * vx - vy * wx) * b = vx * (py - qy) + vy * (qx - px)
#     - b = (vx * (py - qy) + vy * (qx - px)) / (wy * vx - vy * wx)
def intersect(h0, h1):
    ([px, py, pz], [vx, vy, vz]) = h0
    ([qx, qy, qz], [wx, wy, wz]) = h1
    try:
        b = (vx * (py - qy) + vy * (qx - px)) / (wy * vx - vy * wx)
        a = (qx - px + b * wx) / vx
    except ZeroDivisionError:
        return None
    if a < 0 or b < 0:
        return None
    return ((px + a * vx), (py + a * vy))


def count_intersect(low, high):
    c = 0
    for i in range(len(hails)):
        for j in range(i + 1, len(hails)):
            h = intersect(hails[i], hails[j])
            if h is not None and low <= h[0] <= high and low <= h[1] <= high:
                c += 1
    return c


print(
    "Part 1:",
    count_intersect(
        200000000000000 if len(hails) > 5 else 7,
        400000000000000 if len(hails) > 5 else 27,
    ),
)

# Part 2


def find_rock_coordinates():
    # Use SymPy to solve equations on 3 hailstone trajectories.
    px, py, pz, vx, vy, vz = symbols("px,py,pz,vx,vy,vz")
    syms = [px, py, pz, vx, vy, vz]
    eqs = []

    # We need only 3 trajectories, because we have 6 variables for the
    # trajectory we are looking for and we add a single variable for each
    # trajectory we take as input. Keeping 3 of them adds 3 new variables
    # and provides 3 * 3 = 9 equations.
    for i in range(3):
        t = symbols("t" + str(i))
        syms.append(t)
        ([qx, qy, qz], [wx, wy, wz]) = hails[i]
        eqs += [
            Eq(px + t * vx, qx + t * wx),
            Eq(py + t * vy, qy + t * wy),
            Eq(pz + t * vz, qz + t * wz),
        ]

    sols = solve(eqs, syms, dict=True)
    return (
        sols[0][px],
        sols[0][py],
        sols[0][pz],
        sols[0][vx],
        sols[0][vy],
        sols[0][vz],
    )


print("Part 2:", sum(find_rock_coordinates()[0:3]))
