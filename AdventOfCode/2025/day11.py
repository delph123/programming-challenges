from libs import *

# Parse input

devices = [l.split(": ") for l in read_lines("example")]

if read.from_example:
    devices_p2 = {s: t.split() for s, t in devices[devices.index([""]) + 2 :]}
    devices = {s: t.split() for s, t in devices[1 : devices.index([""])]}
else:
    devices = {s: t.split() for s, t in devices}
    devices_p2 = devices

# Part 1


def count_paths(network, source, target):
    paths = {source: 1}
    flows = 0
    while len(paths) > 0:
        flows += paths.get(target, 0)
        paths_to_explore = [(s, n) for s, n in paths.items() if s != target]
        paths = defaultdict(int)
        for s, n in paths_to_explore:
            for t in network.get(s, []):
                paths[t] += n
    return flows


part_one(count_paths(devices, "you", "out"))

# Part 2

cnt_p2 = partial(count_paths, devices_p2)

# Instead of complicating the algorithm, let's count the paths from svr to out by
# splitting it into:
#  - nb(paths from svr to dac) x nb(paths from dac to fft) x nb(paths from fft to out)
#  - nb(paths from svr to fft) x nb(paths from fft to dac) x nb(paths from dac to out)
#
# Note that we should normally count path from svr to dat that do not pass by fft to
# make sure the two counts are disjoint. However, since we know that one of the two
# paths between dac and fft must be impossible (or we would have a cycle), by corollary
# we know that:
#  - either paths(dac, fft) exists and paths(svr, dac) does not go through fft
#  - or paths(fft, dac) exists and path(svr, fft) does not go through dac
#
# Therefore, let's simply add both products and we will be good!

part_two(
    prod(cnt_p2(s, t) for s, t in pairwise(["svr", "dac", "fft", "out"]))
    + prod(cnt_p2(s, t) for s, t in pairwise(["svr", "fft", "dac", "out"]))
)
