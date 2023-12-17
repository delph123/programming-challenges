# Parse input

with open("AdventOfCode/2023/examples/day05.in") as file:
    groups = file.read().strip().split("\n\n")
    seeds = [int(n) for n in groups[0].split(": ")[1].split()]
    mappings = dict()
    maps = dict()
    for map in groups[1:]:
        lines = map.split("\n")
        f, t = lines[0].split(" map")[0].split("-to-")
        mappings[f] = t
        transform = [[int(n) for n in l.split()] for l in lines[1:]]
        maps[f] = transform


# Part 1


def convert(n, f, t):
    cat = f
    num = n
    while cat != t:
        conversions = maps[cat]
        for dest, src, lgth in conversions:
            if num >= src and num < src + lgth:
                num += dest - src
                break
        cat = mappings[cat]

    return num


locations = [convert(n, "seed", "location") for n in seeds]

print("Part 1:", min(locations))

# Part 2


def convert_ranges(rg, f, t):
    cat = f
    ranges = rg
    while cat != t:
        conversions = maps[cat]
        ranges_out = []
        for dest, src, lgth in conversions:
            ranges2 = ranges[:]
            ranges = []
            for rg_start, rg_length in ranges2:
                if rg_start + rg_length - 1 >= src and rg_start <= src + lgth - 1:
                    if rg_start >= src and rg_start + rg_length <= src + lgth:
                        ranges_out.append(((rg_start + dest - src), rg_length))
                    elif rg_start < src and rg_start + rg_length <= src + lgth:
                        lg = src - rg_start
                        ranges.append((rg_start, lg))
                        ranges_out.append((dest, (rg_length - lg)))
                    elif rg_start >= src and rg_start + rg_length > src + lgth:
                        lg = src + lgth - rg_start
                        ranges_out.append(((rg_start + dest - src), lg))
                        ranges.append(((rg_start + lg), (rg_length - lg)))
                    else:
                        lg = src - rg_start
                        ranges.append((rg_start, lg))
                        ranges_out.append((dest, lgth))
                        ranges.append(((src + lgth), (rg_length - lgth - lg)))
                else:
                    ranges.append((rg_start, rg_length))
        ranges_out.extend(ranges)
        ranges = ranges_out[:]
        cat = mappings[cat]

    return ranges


locations = convert_ranges(list(zip(seeds[::2], seeds[1::2])), "seed", "location")

print("Part 2:", min([x for (x, _) in locations]))
