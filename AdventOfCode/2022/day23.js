const {
    part_one,
    part_two,
    readLines,
    deepCopy,
    sum,
} = require("../../common/aoc");

const elves = (function () {
    let e = readLines("example")
        .map((l) => [...l])
        .map((l, j) => l.map((v, i) => (v === "." ? null : elf(j, i))));
    // Keep enough space to grow the map (grow of twice the size necessary to
    // accommodate each elf in its own 3x3 square)
    const BUFFER = Math.ceil(
        Math.sqrt(sum(e.map((l) => l.filter((v) => v !== null).length)) * 10)
    );
    let h = e[0].length + 2 * BUFFER;
    return [
        ...new Array(BUFFER).fill(0).map(() => new Array(h).fill(null)),
        ...e.map((l) => [
            ...new Array(BUFFER).fill(null),
            ...l,
            ...new Array(BUFFER).fill(null),
        ]),
        ...new Array(BUFFER).fill(0).map(() => new Array(h).fill(null)),
    ];
})();

part_one(grove(10));

part_two(run(10000)[1]);

function grove(turns) {
    let e = run(turns)[0];

    let y_min = e.findIndex((l) => l.some((v) => v !== null));
    let y_max = e.findLastIndex((l) => l.some((v) => v !== null));
    let x_min = e[0].findIndex((v, i) => e.some((l) => l[i] !== null));
    let x_max = e[0].findLastIndex((v, i) => e.some((l) => l[i] !== null));

    e = e
        .filter((_, i) => i >= y_min && i <= y_max)
        .map((l) => l.slice(x_min, x_max + 1));

    return sum(e.map((l) => l.filter((v) => v === null).length));
}

function run(turns) {
    let e = deepCopy(elves);

    let allElves = [];
    e.forEach((l, j) => {
        l.forEach((v, i) => {
            if (v !== null) {
                v.i = i;
                v.j = j;
                allElves.push(v);
            }
        });
    });

    let dirs = ["N", "S", "W", "E"];

    for (let t = 0; t < turns; t++) {
        let stop = true;
        let target = new Map();

        // propose & check
        allElves.forEach((elf0) => {
            elf0.prop = standStill(e, elf0.i, elf0.j);
            if (elf0.prop === "?") {
                elf0.prop = makeProp(e, elf0.i, elf0.j, dirs);
            }
            if (elf0.prop !== "0") {
                stop = false;

                let tg = mv(elf0.i, elf0.j, elf0.prop).toString();
                if (target.has(tg)) {
                    target.set(tg, 2);
                } else {
                    target.set(tg, 1);
                }
            }
        });

        if (stop) return [e, t + 1];

        // move
        allElves.forEach((elf0) => {
            if (elf0.prop !== "0") {
                let tg = mv(elf0.i, elf0.j, elf0.prop);
                if (target.get(tg.toString()) === 1) {
                    e[tg[1]][tg[0]] = elf0;
                    e[elf0.j][elf0.i] = null;
                    elf0.i = tg[0];
                    elf0.j = tg[1];
                }
            }
            delete elf0.prop;
        });

        dirs = [...dirs.slice(1), dirs[0]];
    }

    return [e, turns];
}

function elf(j, i) {
    return {};
}

function mv(i, j, dir) {
    if (dir === "N") {
        return [i, j - 1];
    } else if (dir === "S") {
        return [i, j + 1];
    } else if (dir === "W") {
        return [i - 1, j];
    } else if (dir === "E") {
        return [i + 1, j];
    }
}

function standStill(map, i, j) {
    if (map[j - 1].slice(i - 1, i + 2).some((v) => v !== null)) return "?";
    if (map[j + 1].slice(i - 1, i + 2).some((v) => v !== null)) return "?";
    if (map[j][i - 1] !== null || map[j][i + 1] !== null) return "?";
    return "0";
}

function makeProp(map, i, j, dirs) {
    for (let d of dirs) {
        if (propValid(map, i, j, d)) {
            return d;
        }
    }
    return "0";
}

function propValid(map, i, j, dir) {
    if (dir === "N") {
        return (
            map[j - 1][i + 1] === null &&
            map[j - 1][i] === null &&
            map[j - 1][i - 1] === null
        );
    } else if (dir === "S") {
        return (
            map[j + 1][i + 1] === null &&
            map[j + 1][i] === null &&
            map[j + 1][i - 1] === null
        );
    } else if (dir === "W") {
        return (
            map[j - 1][i - 1] === null &&
            map[j][i - 1] === null &&
            map[j + 1][i - 1] === null
        );
    } else if (dir === "E") {
        return (
            map[j - 1][i + 1] === null &&
            map[j][i + 1] === null &&
            map[j + 1][i + 1] === null
        );
    }
}
