/**
 * Day 19: Not Enough Minerals
 *
 * Find maximal number of geode-cracking robots for any blueprint.
 */

const AStarSolver = require("../common/AStarSolver/AStarSolver");
const blueprint = require("./inputs/day19");

const MAX_DURATION = 24;
const MAX_DURATION_P2 = 32;

console.time("total");

let q = 0;
let m = 1;

blueprint.forEach((bp) => {
    console.time("a* " + bp[0]);
    const { path, cost, visited } = collect_astar(bp, [
        MAX_DURATION,
        { ore: 0, clay: 0, obs: 0, geo: 0 },
        { ore: 1, clay: 0, obs: 0, geo: 0 },
    ]);
    console.timeEnd("a* " + bp[0]);

    q += bp[0] * cost;

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
        const { path, cost, visited } = collect_astar(bp, [
            MAX_DURATION_P2,
            { ore: 0, clay: 0, obs: 0, geo: 0 },
            { ore: 1, clay: 0, obs: 0, geo: 0 },
        ]);
        console.timeEnd("a* p2 " + bp[0]);

        m *= cost;

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
console.log("Quality:", q);
console.log("Mult*3:", m);

console.timeEnd("total");

function collect_astar(blueprint, start) {
    const solver = new AStarSolver({
        hash: getHash,
        neighbours: ([turn, collection, robots]) => {
            return [
                getNeighbour(blueprint, turn, collection, robots, 0),
                getNeighbour(blueprint, turn, collection, robots, 1),
                getNeighbour(blueprint, turn, collection, robots, 2),
                getNeighbour(blueprint, turn, collection, robots, 3),
            ].filter((s) => Boolean(s));
        },
        cost: ([ft, fc, fr], [tt, tc, tr], cost) => tc.geo,
        heuristic: ([turn, col, rob], cost) =>
            heuristic(start[0], turn, col, rob),
        compareHeuristic: (a, b) => a - b,
        start: start,
        isGoal: ([turn]) => turn === 0,
    });

    return solver.solve();
}

function heuristic(duration, turn, collection, robots) {
    return collection.geo + turn * robots.geo + (turn * (turn - 1)) / 2;
}

function getHash([turn, col, rob]) {
    return `${rob.ore}/${rob.clay}/${rob.obs}/${rob.geo} | ${col.ore}/${col.clay}/${col.obs}/${col.geo} | ${turn}`;
}

function getNeighbour(
    [bp, ore, clay, ob_ore, ob_clay, geo_ore, geo_obs],
    duration,
    collection,
    robots,
    robot_turn
) {
    let col = { ...collection };
    let rob = { ...robots };

    if (
        exhausted(
            [bp, ore, clay, ob_ore, ob_clay, geo_ore, geo_obs],
            duration,
            collection,
            robots,
            robot_turn
        )
    ) {
        return undefined;
    }

    // Produce
    while (
        duration > 0 &&
        !canCreate(
            [bp, ore, clay, ob_ore, ob_clay, geo_ore, geo_obs],
            col,
            robot_turn
        )
    ) {
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
    [rob, col] = consume(
        [bp, ore, clay, ob_ore, ob_clay, geo_ore, geo_obs],
        rob,
        col,
        robot_turn
    );
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
        // Need to produce geode event during last turn
        // or we won't generate any neighbour during last turn!
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
    robots,
    collection,
    robot_turn
) {
    let col = { ...collection };
    let rob = { ...robots };
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
    return [rob, col];
}
