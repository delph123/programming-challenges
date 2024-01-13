const { part_one, part_two, sum, readLines } = require("../../common/aoc");

const rawRoutes = readLines("e")
    .map((s) => s.split(" -> "))
    .map((a) =>
        a.map((v, i) => v + "-" + a[i + 1]).filter((v, i) => i < a.length - 1)
    );

const routes = rawRoutes
    .flat()
    .sort()
    .filter((v, i, a) => v != a[i - 1])
    .map((r) => r.split("-"))
    .map(([a, b]) =>
        a
            .split(",")
            .concat(b.split(","))
            .map((n) => parseInt(n))
    );

const cave_min_max = [
    Math.min(
        routes.map(([a, b, c, d]) => a).reduce((a, b) => Math.min(a, b), 9999),
        routes.map(([a, b, c, d]) => c).reduce((a, b) => Math.min(a, b), 9999)
    ),
    Math.min(
        routes.map(([a, b, c, d]) => b).reduce((a, b) => Math.min(a, b), 0),
        routes.map(([a, b, c, d]) => d).reduce((a, b) => Math.min(a, b), 0)
    ),
    Math.max(
        routes.map(([a, b, c, d]) => a).reduce((a, b) => Math.max(a, b), -1),
        routes.map(([a, b, c, d]) => c).reduce((a, b) => Math.max(a, b), -1)
    ),
    Math.max(
        routes.map(([a, b, c, d]) => b).reduce((a, b) => Math.max(a, b), -1),
        routes.map(([a, b, c, d]) => d).reduce((a, b) => Math.max(a, b), -1)
    ),
];

const [LEFT, RIGHT, BOTTOM] = [cave_min_max[3] + 3, cave_min_max[3] + 3, 3];

const min_max = [
    cave_min_max[0] - LEFT,
    cave_min_max[1],
    cave_min_max[2] + RIGHT,
    cave_min_max[3] + BOTTOM,
    -cave_min_max[0] + LEFT + cave_min_max[2] + RIGHT,
    cave_min_max[3] + BOTTOM - cave_min_max[1],
];

part_one(sum(cave(1).map((l) => l.filter((a) => a === ".").length)));
part_two(sum(cave(2).map((l) => l.filter((a) => a === ".").length)));

function cave(part) {
    let x_min = min_max[0];

    let grid = new Array(min_max[5])
        .fill(0)
        .map(() => new Array(min_max[4]).fill(" "));

    grid[0][500 - x_min] = "+";
    routes.forEach(([a, b, c, d]) => {
        if (a === c) {
            let fr = Math.min(b, d),
                to = Math.max(b, d);
            for (let i = fr; i <= to; i++) {
                grid[i][a - x_min] = "#";
            }
        } else {
            let fr = Math.min(a, c),
                to = Math.max(a, c);
            for (let i = fr; i <= to; i++) {
                grid[b][i - x_min] = "#";
            }
        }
    });

    while (grid[0][500 - x_min] !== ".") {
        let sand = { x: 500, y: 0 };
        while (
            sand.x > x_min + 1 &&
            sand.x < min_max[2] - 2 &&
            sand.y < min_max[3] - 2
        ) {
            if (grid[sand.y + 1][sand.x - x_min] === " ") {
                sand.y = sand.y + 1;
            } else if (grid[sand.y + 1][sand.x - x_min - 1] === " ") {
                sand.x = sand.x - 1;
                sand.y = sand.y + 1;
            } else if (grid[sand.y + 1][sand.x - x_min + 1] === " ") {
                sand.x = sand.x + 1;
                sand.y = sand.y + 1;
            } else {
                break;
            }
        }

        if (
            part === 1 &&
            !(
                sand.x > x_min + 1 &&
                sand.x < min_max[2] - 2 &&
                sand.y < min_max[3] - 2
            )
        ) {
            break;
        }

        grid[sand.y][sand.x - x_min] = ".";
    }

    return grid;
}
