const {
    part_one,
    part_two,
    read,
    deepCopy,
    product,
} = require("../../common/aoc");

const monkeys = read("example").split("\n\n").map(parseMonkey);

part_one(
    product(
        run_monkey_rounds(20, (wl) => Math.floor(wl / 3))
            .sort((a, b) => b.inspected - a.inspected)
            .slice(0, 2)
            .map((m) => m.inspected)
    )
);

const cond_product = monkeys.map((m) => m.cond).reduce((a, b) => a * b, 1);

part_two(
    product(
        run_monkey_rounds(10000, (wl) => wl % cond_product)
            .sort((a, b) => b.inspected - a.inspected)
            .slice(0, 2)
            .map((m) => m.inspected)
    )
);

function parseMonkey(s) {
    let [m, i, o, c, t, f] = s.split("\n");
    return {
        monkey: m.split("Monkey ")[1].split(":")[0],
        items: i
            .split("Starting items: ")[1]
            .split(", ")
            .map((i) => parseInt(i)),
        op: o
            .split("Operation: new = old ")[1]
            .split(" ")
            .map((v, i) => (i === 1 ? (v === "old" ? "old" : parseInt(v)) : v)),
        cond: parseInt(c.split("  Test: divisible by ")[1]),
        truthy: parseInt(t.split("    If true: throw to monkey ")[1]),
        falsy: parseInt(f.split("    If false: throw to monkey ")[1]),
        inspected: 0,
    };
}

function run_monkey_rounds(ROUNDS, decrease) {
    let mk = deepCopy(monkeys);
    for (let r = 0; r < ROUNDS; r++) {
        mk.forEach((m) => {
            m.items.forEach((it) => {
                let l = decrease(wl(it, m.op));
                let tg = l % m.cond === 0 ? m.truthy : m.falsy;
                mk[tg].items.push(l);
                m.inspected++;
            });
            m.items.length = 0;
        });
    }
    return mk;
}

function wl(it, [op, val]) {
    if (op === "+") return val === "old" ? it + it : it + val;
    if (op === "*") return val === "old" ? it * it : it * val;
}
