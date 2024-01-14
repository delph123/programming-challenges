const { part_one, part_two, readLines } = require("../../common/aoc");

const monkeys = new Map(
    readLines("example")
        .map((a) => a.split(": "))
        .map(([a, b]) => [a, b.split(" ")])
        .map(([a, b]) => [a, b.length === 1 ? parseInt(b[0]) : b])
);

part_one(value("root"));

part_two(find(monkeys.get("root")[0], value_p2(monkeys.get("root")[2], NaN)));

function value(name) {
    let m = monkeys.get(name);
    if (typeof m === "number") return m;
    let [a, b, c] = m;
    let l = value(a);
    let r = value(c);
    if (b === "+") return l + r;
    if (b === "*") return l * r;
    if (b === "-") return l - r;
    if (b === "/") return l / r;
}

function value_p2(name, repl) {
    if (name === "humn") return repl;
    let m = monkeys.get(name);
    if (typeof m === "number") return m;
    let [a, b, c] = m;
    let l = value_p2(a, repl);
    let r = value_p2(c, repl);
    if (b === "+") return l + r;
    if (b === "*") return l * r;
    if (b === "-") return l - r;
    if (b === "/") return l / r;
}

function find(name, value) {
    if (name === "humn") return value;

    let [a, b, c] = monkeys.get(name);
    let l = value_p2(a, NaN);
    let r = value_p2(c, NaN);

    let inv = false;
    let pred;
    if (isNaN(r)) {
        inv = true;
        [a, c] = [c, a];
        [l, r] = [r, l];
    }

    if (b === "+") pred = find(a, value - r);
    if (b === "*") pred = find(a, value / r);
    if (b === "-" && !inv) pred = find(a, value + r);
    if (b === "-" && inv) pred = find(a, r - value);
    if (b === "/" && !inv) pred = find(a, value * r);
    if (b === "/" && inv) pred = find(a, r / value);

    return pred;
}
