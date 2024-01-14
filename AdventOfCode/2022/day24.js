const { part_one, part_two, readLines, deepCopy } = require("../../common/aoc");

const blizz_map = (function () {
    let map = readLines("example");
    map = map
        .map((l) => [...l].filter((v, i, a) => i > 0 && i < a.length - 1))
        .filter((l, i, a) => i > 0 && i < a.length - 1);
    let x_max = map[0].length - 1;
    let y_max = map.length - 1;
    let winds = [].concat(
        ...map.map((l, j) =>
            l
                .map((v, i) => (v === "." ? null : { i, j, dir: v }))
                .filter((v) => v)
        )
    );
    return { map, y_max, x_max, winds };
})();

part_one(escape());
part_two(escape_p2()[2]);

function escape() {
    let bm = deepCopy(blizz_map);
    let start = new Set([str([0, -1])]);
    let end = str([bm.x_max, bm.y_max]);

    let t = 1;
    while (!start.has(end)) {
        bm.winds.forEach((w) => next_blizz(bm, w));
        let avoid = new Set(bm.winds.map((w) => str([w.i, w.j])));
        start = new Set(
            [].concat(...[...start].map((p) => validMoves(bm, p, avoid)))
        );
        t++;
    }

    let out = new Array(bm.y_max + 1)
        .fill(0)
        .map(() => new Array(bm.x_max + 1).fill("."));
    out = bm.winds.reduce((cur, w) => {
        if (cur[w.j][w.i] === ".") {
            cur[w.j][w.i] = w.dir;
        } else if ("<>^v".includes(cur[w.j][w.i])) {
            cur[w.j][w.i] = "2";
        } else {
            cur[w.j][w.i] = `${parseInt(cur[w.j][w.i]) + 1}`;
        }
        return cur;
    }, out);
    out = [...start].map(pos).reduce((cur, [i, j]) => {
        if (j >= 0) {
            if (cur[j][i] !== ".") throw "error";
            cur[j][i] = "E";
        }
        return cur;
    }, out);
    out = out.map((l) => "".concat(...l));

    return t;
}

function escape_p2() {
    let bm = deepCopy(blizz_map);

    let start, end;
    let h = [];
    let t = 1;

    start = new Set([str([0, -1])]);
    end = str([bm.x_max, bm.y_max]);

    while (!start.has(end)) {
        bm.winds.forEach((w) => next_blizz(bm, w));
        let avoid = new Set(bm.winds.map((w) => str([w.i, w.j])));
        start = new Set(
            [].concat(...[...start].map((p) => validMoves(bm, p, avoid)))
        );
        t++;
    }

    h.push(t);
    t++;
    bm.winds.forEach((w) => next_blizz(bm, w));

    start = new Set([str([bm.x_max, bm.y_max + 1])]);
    end = str([0, 0]);

    while (!start.has(end)) {
        bm.winds.forEach((w) => next_blizz(bm, w));
        let avoid = new Set(bm.winds.map((w) => str([w.i, w.j])));
        start = new Set(
            [].concat(...[...start].map((p) => validMoves(bm, p, avoid)))
        );
        t++;
    }

    h.push(t);
    t++;
    bm.winds.forEach((w) => next_blizz(bm, w));

    start = new Set([str([0, -1])]);
    end = str([bm.x_max, bm.y_max]);

    while (!start.has(end)) {
        bm.winds.forEach((w) => next_blizz(bm, w));
        let avoid = new Set(bm.winds.map((w) => str([w.i, w.j])));
        start = new Set(
            [].concat(...[...start].map((p) => validMoves(bm, p, avoid)))
        );
        t++;
    }

    h.push(t);
    return h;
}

function next_blizz(bm, w) {
    if (w.dir === ">") {
        w.i++;
        if (w.i > bm.x_max) w.i = 0;
    } else if (w.dir === "<") {
        w.i--;
        if (w.i < 0) w.i = bm.x_max;
    } else if (w.dir === "v") {
        w.j++;
        if (w.j > bm.y_max) w.j = 0;
    } else if (w.dir === "^") {
        w.j--;
        if (w.j < 0) w.j = bm.y_max;
    }
    return w;
}

function validMoves(bm, s, avoid) {
    let [i, j] = pos(s);
    let r = [[i, j]];
    if (j === -1) {
        r.push([0, 0]);
        return r.map(str).filter((p) => !avoid.has(p));
    }
    if (j === bm.y_max + 1) {
        r.push([bm.x_max, bm.y_max]);
        return r.map(str).filter((p) => !avoid.has(p));
    }
    if (j > 0) r.push([i, j - 1]);
    if (i > 0) r.push([i - 1, j]);
    if (j < bm.y_max) r.push([i, j + 1]);
    if (i < bm.x_max) r.push([i + 1, j]);
    return r.map(str).filter((p) => !avoid.has(p));
}

function str([i, j]) {
    return `${i},${j}`;
}

function pos(s) {
    return s.split(",").map((i) => parseInt(i));
}
