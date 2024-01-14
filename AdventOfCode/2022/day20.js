const { part_one, part_two, readLines } = require("../../common/aoc");

const seq = readLines("example").map((i) => parseInt(i));

const p1 = expand(mix(seq, seq.length), 0);
part_one(p1[1000 % p1.length] + p1[2000 % p1.length] + p1[3000 % p1.length]);

const p2 = expand(
    mix(
        seq.map((n) => n * 811589153),
        10 * seq.length
    ),
    0
);
part_two(p2[1000 % p2.length] + p2[2000 % p2.length] + p2[3000 % p2.length]);

function mix(seq, N) {
    // Prepare
    let entries = seq.map((v, i) => ({ i, v }));
    entries.forEach((o, i, a) => {
        o.n = a[(i + 1) % entries.length];
        o.p = a[(i + entries.length - 1) % entries.length];
    });

    // Mix
    for (let i = 0; i < N; i++) {
        let e = entries[i % entries.length];
        let steps = e.v % (entries.length - 1);

        if (steps === 0) continue;

        // Remove from old position
        let a = e;
        let a1 = e.p;
        let a2 = e.n;
        a1.n = a2;
        a2.p = a1;

        // Search next position
        e = a1;
        for (let j = 0; j < Math.abs(steps); j++) {
            e = Math.sign(steps) > 0 ? e.n : e.p;
        }

        // Insert to new position
        let e2 = e.n;
        e.n = a;
        a.p = e;
        a.n = e2;
        e2.p = a;
    }

    return entries;
}

function expand(mix, from) {
    let r = [];
    let a = mix.find((v) => v.v === from);
    for (let i = 0; i < mix.length; i++) {
        r.push(a.v);
        a = a.n;
    }
    return r;
}
