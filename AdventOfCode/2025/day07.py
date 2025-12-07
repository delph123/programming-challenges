from libs import *

# Parse input

tachyon_manifolds = read_lines("example")
source = tachyon_manifolds[0].find("S")

# Part 1


def split_beam(levels, beams):
    splits = []
    for n, level in enumerate(levels):
        out_beams = set()
        for beam in beams:
            if level[beam] == "^":
                splits.append((n, beam))
                out_beams.add(beam - 1)
                out_beams.add(beam + 1)
            else:
                out_beams.add(beam)
        beams = out_beams
    return splits


part_one(len(split_beam(tachyon_manifolds, set([source]))))

# Part 2


def multi_split_beam(levels, beams: dict[int, int]):
    for level in levels:
        out_beams = defaultdict(int)
        for beam, num in beams.items():
            if level[beam] == "^":
                out_beams[beam - 1] += num
                out_beams[beam + 1] += num
            else:
                out_beams[beam] += num
        beams = out_beams
    return beams


part_two(sum(multi_split_beam(tachyon_manifolds, {source: 1}).values()))
