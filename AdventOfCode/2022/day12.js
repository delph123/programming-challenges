const { part_one, part_two, readLines } = require("../../common/aoc");

const grid = readLines("example");

const heightmap = grid
    .map((l) => [...l].map((s) => s.charCodeAt(0) - "a".charCodeAt(0)))
    .map((l) =>
        l.map((n) =>
            n === "S".charCodeAt(0) - "a".charCodeAt(0)
                ? 0
                : n === "E".charCodeAt(0) - "a".charCodeAt(0)
                ? 25
                : n
        )
    );

const S = [
    grid.map((l) => l.indexOf("S")).findIndex((n) => n >= 0),
    grid.map((l) => l.indexOf("S")).filter((a) => a >= 0)[0],
];
const E = [
    grid.map((l) => l.indexOf("E")).findIndex((n) => n >= 0),
    grid.map((l) => l.indexOf("E")).filter((a) => a >= 0)[0],
];

part_one(path([S]));

const STARTS = heightmap
    .map((l, i) => l.map((v, j) => (v === 0 ? [i, j] : false)).filter((n) => n))
    .flat();

part_two(path(STARTS));

function path(start) {
    const traversed = new Set(start.map(pos));
    let next = start;
    let step = 0;
    while (next.length > 0 && !traversed.has(pos(E))) {
        step++;
        next = uniq(
            next
                .map(reachable)
                .flat()
                .filter((p) => !traversed.has(pos(p)))
        );
        next.forEach((p) => {
            traversed.add(pos(p));
        });
    }
    return step;
}

function reachable(p) {
    let h = heightmap[p[0]][p[1]];
    let r = [];
    if (p[0] > 0 && heightmap[p[0] - 1][p[1]] <= h + 1)
        r.push([p[0] - 1, p[1]]);
    if (p[0] < heightmap.length - 1 && heightmap[p[0] + 1][p[1]] <= h + 1)
        r.push([p[0] + 1, p[1]]);
    if (p[1] > 0 && heightmap[p[0]][p[1] - 1] <= h + 1)
        r.push([p[0], p[1] - 1]);
    if (p[1] < heightmap[p[0]].length - 1 && heightmap[p[0]][p[1] + 1] <= h + 1)
        r.push([p[0], p[1] + 1]);
    return r;
}

function uniq(l) {
    return [...new Set(l.map(pos))].map((s) =>
        s.split("-").map((i) => parseInt(i))
    );
}

function pos(p) {
    return p[0] + "-" + p[1];
}
