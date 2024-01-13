const { part_one, part_two, readLines } = require("../../common/aoc");

const moves = readLines("example")
    .map((l) => l.split(" "))
    .map(([d, s]) => [d, parseInt(s)]);

part_one(new Set(route().map(([a, b]) => `${a},${b}`)).size);
part_two(new Set(route_p2().map(([a, b]) => `${a},${b}`)).size);

function route() {
    let positions = [[0, 0]];
    let h = [0, 0];
    let t = [0, 0];
    for (let [dir, step] of moves) {
        for (let i = 0; i < step; i++) {
            if (dir === "U") {
                h = [h[0], h[1] + 1];
            } else if (dir === "D") {
                h = [h[0], h[1] - 1];
            } else if (dir === "L") {
                h = [h[0] - 1, h[1]];
            } else {
                h = [h[0] + 1, h[1]];
            }

            let d = [Math.abs(t[0] - h[0]), Math.abs(t[1] - h[1])];
            if (d[0] > 1 || d[1] > 1) {
                t = [
                    t[0] + Math.sign(h[0] - t[0]),
                    t[1] + Math.sign(h[1] - t[1]),
                ];
            }

            positions.push(t);
        }
    }
    return positions;
}

function route_p2() {
    let positions = [[0, 0]];
    let h = [0, 0];
    let t = new Array(9).fill(0).map(() => [0, 0]);
    for (let [dir, step] of moves) {
        for (let i = 0; i < step; i++) {
            if (dir === "U") {
                h = [h[0], h[1] + 1];
            } else if (dir === "D") {
                h = [h[0], h[1] - 1];
            } else if (dir === "L") {
                h = [h[0] - 1, h[1]];
            } else {
                h = [h[0] + 1, h[1]];
            }

            for (let j = 0; j < t.length; j++) {
                let u = t[j];
                let v = h;
                if (j > 0) v = t[j - 1];
                let d = [Math.abs(u[0] - v[0]), Math.abs(u[1] - v[1])];
                if (d[0] > 1 || d[1] > 1) {
                    t[j] = [
                        u[0] + Math.sign(v[0] - u[0]),
                        u[1] + Math.sign(v[1] - u[1]),
                    ];
                }
            }

            positions.push(t[t.length - 1]);
        }
    }
    return positions;
}
