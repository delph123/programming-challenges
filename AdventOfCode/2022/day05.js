const { part_one, part_two, read, deepCopy } = require("../../common/aoc");

const stacks_and_moves = read("example").split("\n\n");

const stacks = stacks_and_moves[0]
    .split("\n")
    .map((a) => [...a].filter((_, i) => i % 4 === 1))
    .reverse()
    .slice(1)
    .reduce(
        (a, b) => a.map((s, i) => [...s, b[i - 1]]),
        new Array(stacks_and_moves[0].split("\n").pop().split("   ").length + 1)
            .fill(0)
            .map(() => [])
    )
    .map((a) => a.filter((l) => l && l !== " "));

const movements = stacks_and_moves[1]
    .split("\n")
    .map((a) => a.split("move ")[1].split(" from "))
    .map(([a, b]) => [a, ...b.split(" to ")].map((i) => parseInt(i)));

function top(st) {
    return st
        .slice(1)
        .map((s) => s.pop())
        .join("");
}

function move(st, [n, f, t]) {
    let crate = st[f].pop();
    st[t].push(crate);
    if (n > 1) {
        return move(st, [n - 1, f, t]);
    } else {
        return st;
    }
}

part_one(top(movements.reduce(move, deepCopy(stacks))));

function move9001(st, [n, f, t]) {
    let crates = st[f].splice(-n);
    st[t].push(...crates);
    return st;
}

part_two(top(movements.reduce(move9001, deepCopy(stacks))));
