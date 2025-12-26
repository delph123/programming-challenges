from libs import *

# Parse input

IGNORED_INSTRUCTIONS = ["Step", "must be finished before step", "can begin."]

requirements = [r.split() for r in read_lines("example", ignore=IGNORED_INSTRUCTIONS)]

# Part 1


def step_order(requirements):
    req_by_step = {
        k: set(p for p, _ in v)
        for k, v in groupby(sorted(requirements, key=itemgetter(1)), key=itemgetter(1))
    }
    req_by_step |= {
        k: set() for k in set(s for (s, _) in requirements if s not in req_by_step)
    }
    while req_by_step:
        s = min(k for k, v in req_by_step.items() if len(v) == 0)
        yield s
        del req_by_step[s]
        for r in req_by_step.values():
            if s in r:
                r.remove(s)


part_one(step_order(requirements), sep="")

# Part 2


def duration(workers, step_duration):
    work: list[int] = [None] * workers
    req_by_step = {
        k: set(p for p, _ in v)
        for k, v in groupby(sorted(requirements, key=itemgetter(1)), key=itemgetter(1))
    }
    req_by_step |= {
        k: set() for k in set(s for (s, _) in requirements if s not in req_by_step)
    }
    total_duration = 0
    while req_by_step:
        try:
            s = min(k for k, v in req_by_step.items() if len(v) == 0)
            work[work.index(None)] = (s, step_duration[s])
            del req_by_step[s]
        except ValueError:
            _, d = min((w for w in work if w is not None), key=itemgetter(1))
            total_duration += d
            for i in range(len(work)):
                if work[i] is not None and work[i][1] == d:
                    s0 = work[i][0]
                    work[i] = None
                    for r in req_by_step.values():
                        if s0 in r:
                            r.remove(s0)
                elif work[i] is not None:
                    s0, d0 = work[i]
                    work[i] = (s0, (d0 - d))
    _, remaining = max((w for w in work if w is not None), key=itemgetter(1))
    return total_duration + remaining


base_duration = 0 if read.from_example else 60
step_duration = {chr(i + ord("A")): base_duration + i + 1 for i in range(26)}

part_two(duration(2 if read.from_example else 5, step_duration))
