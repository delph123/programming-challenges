const { part_one, part_two, readLines } = require("../../common/aoc");
const AStarSolver = require("../../common/AStarSolver/AStarSolver");

const blueprints = readLines("example")
    .map((bp) => bp.split(": Each ore robot costs "))
    .map(([a, b]) => [
        parseInt(a.split("Blueprint ")[1]),
        ...b
            .split(" ore. Each clay robot costs ")
            .map((l) => l.split(" ore. Each obsidian robot costs ")),
    ])
    .map(([a, [b], [c, d]]) => [
        a,
        parseInt(b),
        parseInt(c),
        ...d.split(" clay. Each geode robot costs "),
    ])
    .map(([a, b, c, d, e]) => [
        a,
        b,
        c,
        d.split(" ore and "),
        e.split(" obsidian.")[0].split(" ore and "),
    ])
    .map(([a, b, c, [d, e], [f, g]]) => [
        a,
        b,
        c,
        parseInt(d),
        parseInt(e),
        parseInt(f),
        parseInt(g),
    ]);

const MAX_DURATION_PART_1 = 24;
const MAX_DURATION_PART_2 = 32;

console.time("total");

let q = 0;
let m = 1;
let v = 0;
let v2 = 0;

blueprints.forEach((bp) => {
    console.time("a* " + bp[0]);
    const { path, cost, visited } = collect_geodes(bp, [
        MAX_DURATION_PART_1,
        { ore: 0, clay: 0, obs: 0, geo: 0 },
        { ore: 1, clay: 0, obs: 0, geo: 0 },
    ]);
    console.timeEnd("a* " + bp[0]);

    q += bp[0] * cost;
    v += visited;

    console.log(
        "BP",
        bp[0],
        "collected",
        path[path.length - 1][1],
        "using",
        path[path.length - 1][2],
        "cost",
        cost,
        "visited",
        visited
    );

    if (bp[0] < 4) {
        console.time("a* p2 " + bp[0]);
        const { path, cost, visited } = collect_geodes(bp, [
            MAX_DURATION_PART_2,
            { ore: 0, clay: 0, obs: 0, geo: 0 },
            { ore: 1, clay: 0, obs: 0, geo: 0 },
        ]);
        console.timeEnd("a* p2 " + bp[0]);

        m *= cost;
        v2 += visited;

        console.log(
            "BP",
            bp[0],
            "collected",
            path[path.length - 1][1],
            "using",
            path[path.length - 1][2],
            "cost",
            cost,
            "visited",
            visited
        );
    }
});

console.log("--");
console.log("visited:", v, "(total part 1),", v2, "(total part 2)");
console.timeEnd("total");
console.log("--");

part_one(q);
part_two(m);

function collect_geodes(blueprint, start) {
    const solver = new AStarSolver({
        hash: getHash,
        neighbors: ([turn, collection, robots]) => {
            return [
                getNeighbor(blueprint, turn, collection, robots, 0),
                getNeighbor(blueprint, turn, collection, robots, 1),
                getNeighbor(blueprint, turn, collection, robots, 2),
                getNeighbor(blueprint, turn, collection, robots, 3),
            ].filter((s) => s != null);
        },
        cost: ([ft, fc, fr], [tt, tc, tr], cost) => tc.geo,
        heuristic: ([turn, col, rob], cost) =>
            heuristic(blueprint, turn, col, rob),
        compareHeuristic: compareArray,
        start: start,
        isGoal: ([turn, col, rob]) => turn === 0,
    });

    return solver.solve();
}

function compareArray(a, b) {
    for (let i = 0; i < a.length; i++) {
        if (a[i] > b[i]) {
            return 1;
        } else if (a[i] < b[i]) {
            return -1;
        }
    }
    return 0;
}

function heuristic(blueprint, turn, collection, robots) {
    const cols = [0, 1, 2, 3].map(() => ({ ...collection }));
    let rob = { ...robots };
    let d = turn;
    while (d > 0) {
        d--;
        // Check what which robot can be created
        const can = cols.map((col, i) => canCreate(blueprint, col, i));
        // Produce gems on the basis of current robot count
        cols.forEach((col) => {
            col.ore += rob.ore;
            col.clay += rob.clay;
            col.obs += rob.obs;
            col.geo += rob.geo;
        });
        // Create robots
        cols.forEach((col, i) => {
            if (can[i]) {
                consume(blueprint, rob, col, i);
            }
        });
    }
    return [cols[3].geo, -turn];
}

function getHash([turn, col, rob]) {
    return `${rob.ore}/${rob.clay}/${rob.obs}/${rob.geo} | ${col.ore}/${col.clay}/${col.obs}/${col.geo} | ${turn}`;
}

function getNeighbor(blueprint, duration, collection, robots, robot_turn) {
    let col = { ...collection };
    let rob = { ...robots };

    if (exhausted(blueprint, duration, collection, robots, robot_turn)) {
        return undefined;
    }

    // Produce
    while (duration > 0 && !canCreate(blueprint, col, robot_turn)) {
        duration--;
        col.ore += robots.ore;
        col.clay += robots.clay;
        col.obs += robots.obs;
        col.geo += robots.geo;
    }

    if (duration === 0) {
        return [0, col, rob];
    }

    // Create robot
    duration--;
    consume(blueprint, rob, col, robot_turn);
    col.ore += robots.ore;
    col.clay += robots.clay;
    col.obs += robots.obs;
    col.geo += robots.geo;

    return [duration, col, rob];
}

function exhausted(
    [bp, ore, clay, ob_ore, ob_clay, geo_ore, geo_obs],
    duration,
    collection,
    robots,
    robot_turn
) {
    if (robot_turn === 0) {
        let max_ore = Math.max(ore, clay, ob_ore, geo_ore);
        return (
            duration <= 1 ||
            (collection.ore >= max_ore &&
                collection.ore + (duration - 2) * robots.ore >=
                    (duration - 1) * max_ore)
        );
    } else if (robot_turn === 1) {
        return (
            duration <= 1 ||
            (collection.clay >= ob_clay &&
                collection.clay + (duration - 2) * robots.clay >=
                    (duration - 1) * ob_clay)
        );
    } else if (robot_turn === 2) {
        return (
            duration <= 1 ||
            (collection.obs >= geo_obs &&
                collection.obs + (duration - 2) * robots.obs >=
                    (duration - 1) * geo_obs)
        );
    } else {
        // Need to produce geode even during last turn
        // or we won't generate any neighbor during last turn!
        return false;
    }
}

function canCreate(
    [bp, ore, clay, ob_ore, ob_clay, geo_ore, geo_obs],
    col,
    robot_turn
) {
    if (robot_turn === 0) {
        return col.ore >= ore;
    } else if (robot_turn === 1) {
        return col.ore >= clay;
    } else if (robot_turn === 2) {
        return col.ore >= ob_ore && col.clay >= ob_clay;
    } else if (robot_turn === 3) {
        return col.ore >= geo_ore && col.obs >= geo_obs;
    } else {
        return false;
    }
}

function consume(
    [bp, ore, clay, ob_ore, ob_clay, geo_ore, geo_obs],
    rob,
    col,
    robot_turn
) {
    if (robot_turn === 0) {
        col.ore -= ore;
        rob.ore++;
    } else if (robot_turn === 1) {
        col.ore -= clay;
        rob.clay++;
    } else if (robot_turn === 2) {
        col.ore -= ob_ore;
        col.clay -= ob_clay;
        rob.obs++;
    } else if (robot_turn === 3) {
        col.ore -= geo_ore;
        col.obs -= geo_obs;
        rob.geo++;
    }
}
