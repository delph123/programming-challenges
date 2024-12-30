from libs import *

# Parse input

file = "example"

instructions = read_lines(
    file, ignore=["goes to bot ", "gives low to ", "and high to "]
)

bot_values = [l[6:].split(" ") for l in instructions if l.startswith("value")]
bot_values = {
    int(bot): [int(val) for (val, _) in values]
    for bot, values in groupby(sorted(bot_values, key=itemgetter(1)), key=itemgetter(1))
}

bot_instructions = [
    instr[4:].split() for instr in instructions if instr.startswith("bot")
]
bot_instructions = {
    int(bot): ((lk, int(lid)), (hk, int(hid)))
    for bot, lk, lid, hk, hid in bot_instructions
}

# Part 1


def find_bot(detect):
    bots = defaultdict(list) | deepcopy(bot_values)
    bins = defaultdict(list)
    if d := detect(bots, bins):
        return d
    b = max(bots.keys(), key=lambda b: len(bots[b]))
    while len(bots[b]) >= 2:
        for v, (kind, id) in zip(sorted(bots[b]), bot_instructions[b]):
            if kind == "bot":
                bots[id].append(v)
            elif kind == "output":
                bins[id].append(v)
        bots[b].clear()
        if d := detect(bots, bins):
            return d
        b = max(bots.keys(), key=lambda b: len(bots[b]))


def detect_bot_possessing(values):
    def detect_bot(bots, _):
        return next((b for (b, vals) in bots.items() if sorted(vals) == values), None)

    return detect_bot


part_one(find_bot(detect_bot_possessing([17, 61] if file.startswith("i") else [2, 5])))

# Part 2


def detect_bins_by_id(*bin_ids):
    def detect_bins(_, bins):
        if all(b in bins for b in bin_ids):
            return [bins[b] for b in bin_ids]

    return detect_bins


part_two(prod(flatten(find_bot(detect_bins_by_id(0, 1, 2)))))
