const { part_one, part_two, read } = require("../../common/aoc");

const sensors = read("e")
    .replaceAll("Sensor at x=", "")
    .replaceAll(" closest beacon is at x=", "")
    .replaceAll(" y=", "")
    .split("\n")
    .map((a) => a.split(":").map((c) => c.split(",").map((i) => parseInt(i))))
    .map(([s, b]) => ({ s, b, d: manhattan_distance(s, b) }));

const BUFFER = 1000000;

const smap_min_max = [
    max(Math.min, 0),
    max(Math.max, 0),
    max(Math.min, 1),
    max(Math.max, 1),
];

function row(y) {
    return new Array(smap_min_max[1] - smap_min_max[0] + 2 * BUFFER)
        .fill(0)
        .map((_, i) => [smap_min_max[0] + i - BUFFER, y]);
}

function cannot_contain_beacon(p) {
    return (
        !sensors.some((s) => s.b[0] === p[0] && s.b[1] === p[1]) &&
        sensors.some((s) => manhattan_distance(s.s, p) <= s.d)
    );
}

part_one(
    row(sensors.length < 20 ? 10 : 2000000)
        .map(cannot_contain_beacon)
        .filter((a) => a).length
);

part_two(locateLostBeacon(sensors.length < 20 ? 20 : 4000000));

function max(fun, idx) {
    return sensors
        .map((s) => fun(s.s[idx], s.b[idx]))
        .reduce((a, b) => fun(a, b), sensors[0].s[idx]);
}

function manhattan_distance(a, b) {
    return Math.abs(a[0] - b[0]) + Math.abs(a[1] - b[1]);
}

function locateLostBeacon(cmax) {
    for (let i = 0; i <= cmax; i++) {
        for (let j = 0; j <= cmax; j++) {
            let b = sensors.reduce(
                (m, s) => Math.max(m, s.d - manhattan_distance(s.s, [i, j])),
                -1
            );
            if (b < 0) {
                return 4000000 * i + j;
            }
            j += b;
        }
    }
}
