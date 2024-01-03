# Parse input

speeds = [
    l.replace("can fly ", "")
    .replace("km/s for ", "")
    .replace("seconds, but then must rest for ", "")
    .replace(" seconds.", "")
    .split(" ")
    for l in open("AdventOfCode/2015/inputs/day14.in").read().strip().split("\n")
]

speeds = {
    reindeer: (int(speed), int(duration), int(rest))
    for (reindeer, speed, duration, rest) in speeds
}

# Part 1


def distance(reindeer, duration):
    speed, dur, rest = speeds[reindeer]
    bursts = duration // (dur + rest)
    remainder = duration % (dur + rest)
    if remainder >= dur:
        return (bursts + 1) * speed * dur
    else:
        return bursts * speed * dur + remainder * speed


print("Part 1:", max([distance(r, 2503) for r in speeds.keys()]))

# Part 2


def race(duration):
    reindeers = list(speeds.keys())
    points = {r: 0 for r in reindeers}
    dist = {r: 0 for r in reindeers}
    for d in range(duration):
        for reindeer in reindeers:
            speed, dur, rest = speeds[reindeer]
            remainder = d % (dur + rest)
            dist[reindeer] += speed if remainder < dur else 0
        winner = max(dist.values())
        for reindeer in reindeers:
            points[reindeer] += 1 if dist[reindeer] == winner else 0
    return points


print("Part 2:", max(race(2503).values()))
