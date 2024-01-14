const { part_one, part_two, readLines } = require("../../common/aoc");

const cubes = new Set(readLines("example"));
const lava = [...cubes].map(pos);

const SCOPE = lava.reduce(
    ({ xmin, xmax, ymin, ymax, zmin, zmax }, [a, b, c]) => ({
        xmin: Math.min(xmin, a),
        ymin: Math.min(ymin, b),
        zmin: Math.min(zmin, c),
        xmax: Math.max(xmax, a),
        ymax: Math.max(ymax, b),
        zmax: Math.max(zmax, c),
    }),
    { xmin: 16, xmax: 16, ymin: 8, ymax: 8, zmin: 5, zmax: 5 }
);

const adjacents = lava
    .map(([a, b, c]) => [
        [a + 1, b, c],
        [a - 1, b, c],
        [a, b + 1, c],
        [a, b - 1, c],
        [a, b, c + 1],
        [a, b, c - 1],
    ])
    .map((sides) => sides.filter((p) => !cubes.has(str(p))))
    .flat();

part_one(adjacents.length);

part_two(exteriors());

function exteriors() {
    const [interior, exterior] = [new Set(), new Set()];

    adjacents.forEach((p) =>
        investigate(interior, exterior, p, new Set(), 100)
    );

    return adjacents.map(str).filter((s) => !interior.has(s)).length;
}

function investigate(interior, exterior, [a, b, c], avoid, step) {
    let abcstr = str([a, b, c]);
    if (interior.has(abcstr) || exterior.has(abcstr)) {
        return;
    }

    let adj = [
        [a + 1, b, c],
        [a - 1, b, c],
        [a, b + 1, c],
        [a, b - 1, c],
        [a, b, c + 1],
        [a, b, c - 1],
    ]
        .map(str)
        .filter((l) => !avoid.has(l))
        .filter((l) => !cubes.has(l))
        .map(pos);

    if (adj.length === 0) {
        interior.add(abcstr);
        return;
    }

    for (let [i, j, k] of adj) {
        let s = str([i, j, k]);
        if (interior.has(s)) {
            interior.add(abcstr);
            return;
        } else if (exterior.has(s)) {
            exterior.add(abcstr);
            return;
        } else if (
            i < SCOPE.xmin ||
            i > SCOPE.xmax ||
            j < SCOPE.ymin ||
            j > SCOPE.ymax ||
            k < SCOPE.zmin ||
            k > SCOPE.zmax
        ) {
            exterior.add(s);
            exterior.add(abcstr);
            return;
        }
    }

    let w = "";

    if (avoid.size < step) {
        for (let [i, j, k] of adj) {
            let s = str([i, j, k]);
            investigate(
                interior,
                exterior,
                [i, j, k],
                new Set([...avoid, abcstr]),
                step
            );
            if (exterior.has(s)) {
                w = "ext";
                break;
            } else if (interior.has(s)) {
                w = "int";
            }
        }
        if (w === "ext") {
            for (let pp of adj) {
                interior.delete(str(pp));
                exterior.add(str(pp));
            }
            exterior.add(abcstr);
            return;
        } else if (w === "int") {
            for (let pp of adj) {
                interior.add(str(pp));
            }
            interior.add(abcstr);
            return;
        }
    }
}

function str([x, y, z]) {
    return `${x},${y},${z}`;
}

function pos(s) {
    return s.split(",").map((i) => parseInt(i));
}
