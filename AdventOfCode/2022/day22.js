const { part_one, part_two, read } = require("../../common/aoc");

const cube_instr = read("example").split("\n\n");

const instructions = [
    cube_instr[0].split("\n").map((l) => [...l]),
    split(cube_instr[1], "L")
        .map((o) => split(o, "R"))
        .flat()
        .map((v, i) => (i % 2 === 0 ? parseInt(v) : v)),
];

// Part 1

const [pos_p1, dir_p1] = (function () {
    let [map, path] = instructions;

    let pos = [0, map[0].findIndex((n) => n !== " ")];
    let dir = [0, 1];

    for (let t = 0; t < path.length; t++) {
        let pt = path[t];
        if (typeof pt === "number") {
            for (let u = 0; u < pt; u++) {
                let n = next(map, pos, dir);
                if (map[n[0]][n[1]] === "#") {
                    break;
                } else if (map[n[0]][n[1]] === ".") {
                    pos = n;
                } else {
                    throw "error";
                }
            }
        } else {
            dir = turn(dir, pt);
        }
    }

    return [pos, dir];
})();

part_one(password(pos_p1, dir_p1));

function password(pos, dir) {
    const DIRS = { "01": 0, "0-1": 2, 10: 1, "-10": 3 };
    return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + DIRS[dir.join("")];
}

function split(s, h) {
    let r = s
        .split(h)
        .map((t) => [t, h])
        .flat();
    r.pop();
    return r;
}

function next(map, [a, b], [c, d]) {
    let n = [a + c, b + d];
    if (
        n[0] < 0 ||
        n[0] >= map.length ||
        n[1] < 0 ||
        n[1] >= map[n[0]].length ||
        map[n[0]][n[1]] === " "
    ) {
        if (c === 0 && d === 1) return [a, map[a].findIndex((n) => n !== " ")];
        if (c === 1 && d === 0)
            return [
                map.findIndex((line) => b < line.length && line[b] !== " "),
                b,
            ];
        if (c === 0 && d === -1)
            return [a, map[a].findLastIndex((n) => n !== " ")];
        if (c === -1 && d === 0)
            return [
                map.findLastIndex((line) => b < line.length && line[b] !== " "),
                b,
            ];
    }
    return n;
}

function turn([a, b], dir) {
    if (dir === "R") {
        if (a === 0 && b === 1) return [1, 0];
        if (a === 1 && b === 0) return [0, -1];
        if (a === 0 && b === -1) return [-1, 0];
        if (a === -1 && b === 0) return [0, 1];
    } else {
        if (a === 0 && b === 1) return [-1, 0];
        if (a === 1 && b === 0) return [0, 1];
        if (a === 0 && b === -1) return [1, 0];
        if (a === -1 && b === 0) return [0, -1];
    }
}

// Part 2

/*
 * The characteristics below is for this kind of pattern:
 *
 * -12-
 * -0--
 * 43--
 * 5---
 *
 * Other kinds of patterns won't work with that!
 */
let CHARACS = {
    size: 50,
    faces: [, 1, 2, , , 0, , , 4, 3, , , 5],
    coord: [
        [50, 50],
        [0, 50],
        [0, 100],
        [100, 50],
        [100, 0],
        [150, 0],
    ],
    next: [
        new Map([
            ["1,0", { face: 3, dir: [1, 0], for: "down" }],
            ["0,-1", { face: 4, dir: [1, 0], for: "left" }],
            ["-1,0", { face: 1, dir: [-1, 0], for: "up" }],
            ["0,1", { face: 2, dir: [-1, 0], for: "right" }],
        ]),
        new Map([
            ["1,0", { face: 0, dir: [1, 0], for: "down" }],
            ["0,-1", { face: 4, dir: [0, 1], for: "left" }],
            ["-1,0", { face: 5, dir: [0, 1], for: "up" }],
            ["0,1", { face: 2, dir: [0, 1], for: "right" }],
        ]),
        new Map([
            ["1,0", { face: 0, dir: [0, -1], for: "down" }],
            ["0,-1", { face: 1, dir: [0, -1], for: "left" }],
            ["-1,0", { face: 5, dir: [-1, 0], for: "up" }],
            ["0,1", { face: 3, dir: [0, -1], for: "right" }],
        ]),
        new Map([
            ["1,0", { face: 5, dir: [0, -1], for: "down" }],
            ["0,-1", { face: 4, dir: [0, -1], for: "left" }],
            ["-1,0", { face: 0, dir: [-1, 0], for: "up" }],
            ["0,1", { face: 2, dir: [0, -1], for: "right" }],
        ]),
        new Map([
            ["1,0", { face: 5, dir: [1, 0], for: "down" }],
            ["0,-1", { face: 1, dir: [0, 1], for: "left" }],
            ["-1,0", { face: 0, dir: [0, 1], for: "up" }],
            ["0,1", { face: 3, dir: [0, 1], for: "right" }],
        ]),
        new Map([
            ["1,0", { face: 2, dir: [1, 0], for: "down" }],
            ["0,-1", { face: 1, dir: [1, 0], for: "left" }],
            ["-1,0", { face: 4, dir: [-1, 0], for: "up" }],
            ["0,1", { face: 3, dir: [-1, 0], for: "right" }],
        ]),
    ],
};

if (instructions[0].length < 20) {
    /*
     * This is the characteristics for the example pattern:
     *
     * --1-
     * 540-
     * --32
     */
    CHARACS = {
        size: 4,
        faces: [, , 1, , 5, 4, 0, , , , 3, 2],
        coord: [
            [4, 8],
            [0, 8],
            [8, 12],
            [8, 8],
            [4, 4],
            [4, 0],
        ],
        next: [
            new Map([
                ["1,0", { face: 3, dir: [1, 0], for: "down" }],
                ["0,-1", { face: 4, dir: [0, -1], for: "left" }],
                ["-1,0", { face: 1, dir: [-1, 0], for: "up" }],
                ["0,1", { face: 2, dir: [1, 0], for: "right" }],
            ]),
            new Map([
                ["1,0", { face: 0, dir: [1, 0], for: "down" }],
                ["0,-1", { face: 4, dir: [1, 0], for: "left" }],
                ["-1,0", { face: 5, dir: [1, 0], for: "up" }],
                ["0,1", { face: 2, dir: [0, -1], for: "right" }],
            ]),
            new Map([
                ["1,0", { face: 5, dir: [0, 1], for: "down" }],
                ["0,-1", { face: 3, dir: [0, -1], for: "left" }],
                ["-1,0", { face: 0, dir: [0, -1], for: "up" }],
                ["0,1", { face: 1, dir: [0, -1], for: "right" }],
            ]),
            new Map([
                ["1,0", { face: 5, dir: [-1, 0], for: "down" }],
                ["0,-1", { face: 4, dir: [-1, 0], for: "left" }],
                ["-1,0", { face: 0, dir: [-1, 0], for: "up" }],
                ["0,1", { face: 2, dir: [0, 1], for: "right" }],
            ]),
            new Map([
                ["1,0", { face: 3, dir: [0, 1], for: "down" }],
                ["0,-1", { face: 5, dir: [0, -1], for: "left" }],
                ["-1,0", { face: 1, dir: [0, 1], for: "up" }],
                ["0,1", { face: 0, dir: [0, 1], for: "right" }],
            ]),
            new Map([
                ["1,0", { face: 3, dir: [-1, 0], for: "down" }],
                ["0,-1", { face: 2, dir: [-1, 0], for: "left" }],
                ["-1,0", { face: 1, dir: [1, 0], for: "up" }],
                ["0,1", { face: 4, dir: [0, 1], for: "right" }],
            ]),
        ],
    };
}

const [pos_p2, dir_p2] = (function () {
    let [map, path] = instructions;

    let pos = [0, map[0].findIndex((n) => n !== " ")];
    let dir = [0, 1];

    for (let t = 0; t < path.length; t++) {
        let pt = path[t];
        if (typeof pt === "number") {
            for (let u = 0; u < pt; u++) {
                let [n, dn] = next_face(CHARACS, pos, dir);
                if (map[n[0]][n[1]] === "#") {
                    break;
                } else if (map[n[0]][n[1]] === ".") {
                    pos = n;
                    dir = dn;
                } else {
                    throw "error";
                }
            }
        } else {
            dir = turn(dir, pt);
        }
    }

    return [pos, dir];
})();

part_two(password(pos_p2, dir_p2));

function next_face(characs, [j, i], dir) {
    let [y, x, yr, xr] = [
        Math.floor(j / characs.size),
        Math.floor(i / characs.size),
        j % characs.size,
        i % characs.size,
    ];
    if (
        yr + dir[0] >= 0 &&
        yr + dir[0] < characs.size &&
        xr + dir[1] >= 0 &&
        xr + dir[1] < characs.size
    ) {
        return [[j + dir[0], i + dir[1]], dir];
    }
    let nf = characs.next[characs.faces[4 * y + x]].get(dir.toString());
    let a, b;
    if (nf.dir[0] === 1) {
        if (dir[0] === 1) a = xr;
        if (dir[0] === -1) a = characs.size - 1 - xr;
        if (dir[1] === 1) a = characs.size - 1 - yr;
        if (dir[1] === -1) a = yr;
        b = 0;
    }
    if (nf.dir[0] === -1) {
        if (dir[0] === 1) a = characs.size - 1 - xr;
        if (dir[0] === -1) a = xr;
        if (dir[1] === 1) a = yr;
        if (dir[1] === -1) a = characs.size - 1 - yr;
        b = characs.size - 1;
    }
    if (nf.dir[1] === 1) {
        a = 0;
        if (dir[0] === 1) b = characs.size - 1 - xr;
        if (dir[0] === -1) b = xr;
        if (dir[1] === 1) b = yr;
        if (dir[1] === -1) b = characs.size - 1 - yr;
    }
    if (nf.dir[1] === -1) {
        a = characs.size - 1;
        if (dir[0] === 1) b = xr;
        if (dir[0] === -1) b = characs.size - 1 - xr;
        if (dir[1] === 1) b = characs.size - 1 - yr;
        if (dir[1] === -1) b = yr;
    }
    return [
        [characs.coord[nf.face][0] + b, characs.coord[nf.face][1] + a],
        nf.dir,
    ];
}
