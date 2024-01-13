const { readLines, sum, part_one, part_two } = require("../../common/aoc");

const rucksacks = readLines("example");

const priorities = rucksacks
    .map((a) => [a.substring(0, a.length / 2), a.substring(a.length / 2)])
    .map(([a, b]) => [new Set([...a]), new Set([...b])])
    .map(([c, d]) => [...d].filter((n) => c.has(n)))
    .map((e) => (e.length === 1 ? priority(e[0]) : -1));

function priority(a) {
    if (a >= "a") {
        return a.charCodeAt(0) - 96;
    } else {
        return a.charCodeAt(0) - 38;
    }
}

part_one(sum(priorities));

const items = rucksacks.map((s) => new Set([...s]));

const groups = items
    .reduce(
        (a, s, i) => {
            a[Math.floor(i / 3)].push(s);
            return a;
        },
        new Array(items.length / 3).fill(0).map(() => [])
    )
    .map(([a, b, c]) => [...a].filter((k) => b.has(k)).filter((k) => c.has(k)))
    .map((a) => (a.length === 1 ? priority(a[0]) : -1));

part_two(sum(groups));
