const { part_one, part_two, readLines, sum } = require("../../common/aoc");

const operations = readLines("example")
    .map((f) =>
        f.startsWith("addx") ? ["addx", parseInt(f.split("addx ")[1])] : [f]
    )
    .flat()
    .map((l, i) => ({ op: l, add: typeof l === "number" ? l : 0, i }))
    .reduce(
        (a, { op, add, i }) => [
            ...a,
            { i: i + 2, op, add, r: add + a[a.length - 1].r },
        ],
        [{ i: 1, op: "noop", add: 0, r: 1 }]
    );

const strengths = operations
    .filter((l, n) => (l.i + 20) % 40 === 0)
    .map((l) => l.i * l.r);

part_one(sum(strengths));

const pixels = operations.map((l) => ({
    i: l.i,
    r: l.r,
    n: ((l.i - 1) % 40) + 1,
    v: Math.abs(((l.i - 1) % 40) + 1 - l.r - 1) <= 1 ? "#" : ".",
}));

part_two(
    new Array(6)
        .fill(0)
        .map(() => new Array(40).fill(0))
        .map((l, i) => l.map((_, j) => pixels[40 * i + j].v).join(""))
);
