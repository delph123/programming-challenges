/**
 * Day 17:
 *
 * .
 */

const movements = require("./inputs/day17");

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

const [grid, highest, spliced, cycle] = tetris(SHAPES, movements, 1_000_000);
console.log(grid, highest, spliced, cycle);

function tetris(shapes, movements, numberOfTurns) {
    let grid = new Array(Y_MAX).fill(0).map(() => new Array(X_MAX).fill(0));
    let h_spliced = 0;
    let highest = new Array(X_MAX).fill(-1);
    let cycle = { step: -1, nb: 0, shapes: new Map() };

    for (let round = 0; round < numberOfTurns; round++) {
        let s = shapes[round % shapes.length];
        let h_max = highest.reduce((a, b) => Math.max(a, b), -1);
        let px = 2;
        let py = h_max + 4;

        // descent
        let stopped = false;
        while (!stopped) {
            // push
            cycle.step = (cycle.step + 1) % movements.length;

            // Detect cycle
            if (cycle.step === 0) {
                cycle.nb++;
                let h_min = highest.reduce(
                    (a, b) => Math.min(a, b),
                    highest[0]
                );
                let fingerprint = `${round % shapes.length}:${py - h_max}/${
                    py - h_min
                }:${highest.map((n) => n - h_min)}`;
                if (!cycle.shapes.has(fingerprint)) {
                    cycle.shapes.set(fingerprint, []);
                }
                cycle.shapes.set(fingerprint, [
                    h_min + h_spliced,
                    ...cycle.shapes.get(fingerprint),
                ]);
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

        // Splice array to avoid consuming to much memory
        if (round % 100_000 === 0) {
            let min = highest.reduce((a, b) => Math.min(a, b), highest[0]);
            if (min > 0) {
                grid = new Array(Y_MAX)
                    .fill(0)
                    .map((_, i) =>
                        i + min < Y_MAX
                            ? grid[i + min]
                            : new Array(X_MAX).fill(0)
                    );
                h_spliced += min;
                highest = highest.map((n) => n - min);
            }
        }
    }

    return [grid, highest, h_spliced, cycle];
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
