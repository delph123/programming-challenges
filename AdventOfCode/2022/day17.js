const { part_one, part_two, read } = require("../../common/aoc");

const movements = read("example");

const X_MAX = 7;
const Y_MAX = 1_000_000;

const SHAPES = [
    [[1, 1, 1, 1]],
    [
        [0, 2, 0],
        [2, 2, 2],
        [0, 2, 0],
    ],
    [
        [3, 3, 3],
        [0, 0, 3],
        [0, 0, 3],
    ],
    [[4], [4], [4], [4]],
    [
        [5, 5],
        [5, 5],
    ],
];

part_one(tetris(SHAPES, movements, 2022n).toString());
part_two(tetris(SHAPES, movements, 1000000000000n).toString());

function tetris(shapes, movements, numberOfTurns) {
    let grid = new Array(Y_MAX).fill(0).map(() => new Array(X_MAX).fill(0));
    let h_spliced = 0n;
    let highest = new Array(X_MAX).fill(-1);
    let cycle = { step: -1, nb: 0, shapes: new Map() };

    for (let round = 0n; round < numberOfTurns; round++) {
        let s = shapes[Number(round % BigInt(shapes.length))];
        let h_max = highest.reduce((a, b) => Math.max(a, b), -1);
        let px = 2;
        let py = h_max + 4;

        // descent
        let stopped = false;
        while (!stopped) {
            // push
            cycle.step = (cycle.step + 1) % movements.length;

            // Detect cycle
            if (h_spliced == 0n && cycle.step === 0) {
                cycle.nb++;
                let h_min = highest.reduce(
                    (a, b) => Math.min(a, b),
                    highest[0]
                );
                let fingerprint = `${round % BigInt(shapes.length)}:${
                    py - h_max
                }/${py - h_min}:${highest.map((n) => n - h_min)}`;
                if (!cycle.shapes.has(fingerprint)) {
                    cycle.shapes.set(fingerprint, [h_min, round]);
                } else {
                    // We have identified a cycle:
                    //  - the cycle has a duration of (round - t1)
                    //  - the gain in min height for each cycle is (h_min - h1)
                    let [h1, t1] = cycle.shapes.get(fingerprint);
                    // we can compute how many cycles will be necessary to
                    // complete the requested number of turns
                    let cycles = (numberOfTurns - t1) / (round - t1);
                    // and fast-forward in the future
                    round += (cycles - 1n) * (round - t1);
                    // adding as many height as necessary
                    h_spliced = (cycles - 1n) * BigInt(h_min - h1);
                }
            }

            // Move if possible
            let m = movements[cycle.step] === ">" ? 1 : -1;
            if (allowed(grid, s, px + m, py)) {
                px += m;
            }

            // Fall while possible
            if (allowed(grid, s, px, py - 1)) {
                py = py - 1;
            } else {
                stopped = true;
            }
        }

        // Draw shape on grid
        for (let j = 0; j < s.length; j++) {
            for (let i = 0; i < s[j].length; i++) {
                grid[j + py][i + px] += s[j][i];
                if (s[j][i] > 0 && highest[i + px] < j + py) {
                    highest[i + px] = j + py;
                }
            }
        }
    }

    return h_spliced + BigInt(Math.max(...highest) + 1);
}

function allowed(grid, shape, px, py) {
    if (py < 0 || px < 0 || px + shape[0].length >= X_MAX + 1) {
        return false;
    }
    for (let j = 0; j < shape.length; j++) {
        for (let i = 0; i < shape[j].length; i++) {
            if (grid[j + py][i + px] * shape[j][i] !== 0) {
                return false;
            }
        }
    }
    return true;
}
