from libs import *

# Parse input

rules = [l.split(" => ") for l in read_lines("example")]

rules_2_3 = [tuple(r.replace("/", "") for r in [a, b]) for a, b in rules if len(a) == 5]
rules_3_4 = [
    tuple(r.replace("/", "") for r in [a, b]) for a, b in rules if len(a) == 11
]

# Normalize mapping


def normalize_2x2(t, reversed=False):
    return "".join(t[i] for i in [0, 1, 3, 2])


def normalize_3x3(t, reversed=False):
    if not reversed:
        return "".join(t[i] for i in [0, 1, 2, 5, 8, 7, 6, 3, 4])
    else:
        return "".join(t[i] for i in [0, 1, 2, 7, 8, 3, 6, 5, 4])


def flipped(t):
    return t[:1] + t[2 * (len(t) // 2) - 1 : 0 : -1] + t[2 * (len(t) // 2) :]


def rotated(t):
    suffix = t[2 * (len(t) // 2) :]
    t = t[: 2 * (len(t) // 2)]
    for i in range(0, len(t), len(t) // 4):
        yield t[-i:] + t[:-i] + suffix


def enhanced_rule_mapping(rules, normalize):
    m = {}
    for k, v in rules:
        for n in [normalize(k), flipped(normalize(k))]:
            for r in rotated(n):
                m[normalize(r, reversed=True)] = v
    return m


enhance_2_3 = enhanced_rule_mapping(rules_2_3, normalize_2x2)
enhance_3_4 = enhanced_rule_mapping(rules_3_4, normalize_3x3)

# Part 1


def split_to_2_square(t):
    s = int(sqrt(len(t) // 4))
    return [
        f"{t[x]}{t[x+1]}{t[x+2*s]}{t[x+2*s+1]}"
        for n in range(0, 4 * s * s, 4 * s)
        for x in range(n, n + 2 * s, 2)
    ]


def merge_3x3(texts):
    u = list(range(36))
    for o, t in zip([0, 3, 18, 21], texts):
        for i, j in product(range(3), range(3)):
            u[o + 6 * j + i] = t[3 * j + i]
    return u


@cache
def enhance_3x3(s3x3):
    s2x2_list = split_to_2_square(enhance_3_4[s3x3])
    s6x6 = merge_3x3([enhance_2_3[s] for s in s2x2_list])
    return Counter([enhance_2_3[s] for s in split_to_2_square(s6x6)])


def map_counter(cnt: Counter[str], mapping):
    m1 = Counter()
    for s, c1 in cnt.items():
        for k, c2 in mapping(s).items():
            m1[k] += c1 * c2
    return m1


def enhance(s3x3, times):
    s3x3_mapping = Counter({s3x3: 1})
    for _ in range(times // 3):
        s3x3_mapping = map_counter(s3x3_mapping, enhance_3x3)
    if times % 3 >= 1:
        s3x3_mapping = map_counter(
            s3x3_mapping, lambda s: Counter(split_to_2_square(enhance_3_4[s]))
        )
    if times % 3 >= 2:
        s3x3_mapping = map_counter(s3x3_mapping, lambda s: Counter({enhance_2_3[s]: 1}))
    return s3x3_mapping


def count_pixels(cnt: Counter[str], p):
    return sum([s.count(p) * c for s, c in cnt.items()])


# Part 1 & 2

if read.from_example:
    part_one(count_pixels(enhance(".#...####", 2), "#"))
    part_two("not enough mapping in example for second part")
else:
    part_one(count_pixels(enhance(".#...####", 5), "#"))
    part_two(count_pixels(enhance(".#...####", 18), "#"))
