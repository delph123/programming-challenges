from libs import *
from datetime import datetime, timedelta

# Parse input

matcher = create_matcher(
    [
        (r"\[{str*}\] Guard #{int} begins shift", ("guard", 0, 1)),
        (r"\[{str*}\] falls asleep", ("sleep", 0, ())),
        (r"\[{str*}\] wakes up", ("wakes", 0, ())),
    ]
)

records = [matcher(l) for l in sorted(read_lines("example"))]
records = [(t, datetime.strptime(d, "%Y-%m-%d %H:%M"), g) for (t, d, g) in records]

# Add 1 hour because some records starts the day before at 23:XX
guards = {(d + timedelta(0, 3600)).date(): g for (t, d, g) in records if t == "guard"}

day_records = {
    d: list(r)
    for d, r in groupby(
        ((t, d) for (t, d, _) in records if t != "guard"), lambda r: r[1].date()
    )
}

day_records_by_guards = {
    g: [day_records.get(d, []) for d, _ in days]
    for g, days in groupby(sorted(guards.items(), key=itemgetter(1)), key=itemgetter(1))
}

# Part 1


def sleep_duration(records):
    return sum(
        (w - s).seconds // 60 for (_, s), (_, w) in zip(records[::2], records[1::2])
    )


def most_asleep(day_records):
    minutes = [0 for _ in range(60)]
    for records in day_records:
        for (_, s), (_, w) in zip(records[::2], records[1::2]):
            for m in range(s.minute, w.minute):
                minutes[m] += 1
    return max(enumerate(minutes), key=itemgetter(1))


def strategy_1():
    (g, dr) = max(
        day_records_by_guards.items(),
        key=lambda x: sum(sleep_duration(r) for r in x[1]),
    )
    return g * most_asleep(dr)[0]


part_one(strategy_1())

# Part 2


def strategy_2():
    best_minutes = {g: most_asleep(dr) for g, dr in day_records_by_guards.items()}
    return max([(g * m, d) for g, (m, d) in best_minutes.items()], key=itemgetter(1))[0]


part_two(strategy_2())
