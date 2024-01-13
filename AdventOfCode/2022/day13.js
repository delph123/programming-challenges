const { part_one, part_two, sum, read } = require("../../common/aoc");

const messages_file = read("example");

const ordered_indices = messages_file
    .split("\n\n")
    .map((b) => b.split("\n").map((js) => JSON.parse(js)))
    .map(([a, b], i) => (comparePackets(a, b) < 0 ? i + 1 : 0));

part_one(sum(ordered_indices));

const orderedMessages = [
    ...messages_file
        .split("\n")
        .filter((s) => s.length > 0) // remove empty lines
        .map((js) => JSON.parse(js)),
    [[2]],
    [[6]],
]
    .sort(comparePackets)
    .map((s) => JSON.stringify(s));

part_two(
    (orderedMessages.findIndex((s) => s === "[[2]]") + 1) *
        (orderedMessages.findIndex((s) => s === "[[6]]") + 1)
);

function comparePackets(l, r) {
    if (Array.isArray(l) && Array.isArray(r)) {
        if (l.length === 0 && r.length > 0) return -1;
        else if (l.length === 0 && r.length === 0) return 0;
        else if (l.length > 0 && r.length === 0) return 1;
        else {
            let o = comparePackets(l[0], r[0]);
            if (o !== 0) return o;
            else return comparePackets(l.slice(1), r.slice(1));
        }
    } else if (Array.isArray(l)) {
        return comparePackets(l, [r]);
    } else if (Array.isArray(r)) {
        return comparePackets([l], r);
    } else {
        return l - r;
    }
}
