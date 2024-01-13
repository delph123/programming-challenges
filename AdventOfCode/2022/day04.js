const { readLines, part_one, part_two } = require("../../common/aoc");

const pairs = readLines("example").map((a) =>
    a.split(",").map((p) => p.split("-").map((i) => parseInt(i)))
);

function includes([a, b], [c, d]) {
    return (a <= c && b >= d) || (c <= a && d >= b);
}

part_one(pairs.filter(([p1, p2]) => includes(p1, p2)).length);

function overlap([a, b], [c, d]) {
    return a <= d && b >= c;
}

part_two(pairs.filter(([p1, p2]) => overlap(p1, p2)).length);
