const { part_one, part_two, readLines } = require("../../common/aoc");
const AStarSolver = require("../../common/AStarSolver/AStarSolver");

const nodes = readLines("example")
    .map((line) =>
        line
            .replace("valves", "valve")
            .replace("tunnels", "tunnel")
            .replace("leads", "lead")
            .split("; tunnel lead to valve ")
    )
    .map(([a, b]) => [...a.split(" has flow rate="), b.split(", "), b])
    .map(([a, b, c, d]) => ({
        id: a.split("Valve ")[1],
        flow: parseInt(b),
        links: c,
    }))
    .sort((a, b) => b.flow - a.flow);

// Compute a reduction of the graph composed of only meaningful nodes
// (with a strictly positive flow) plus the starting point
const relevant_nodes = nodes
    .map((nd) => ({ ...nd, links: nd.links.map((ll) => next(nd, ll)) }))
    .filter((nd) => nd.id === "AA" || nd.flow > 0);
// Replace links to point to nodes from relevant_nodes itself
relevant_nodes.forEach((nd) => {
    nd.links = nd.links.map(([n, l]) => [
        relevant_nodes.find((e) => e.id === n.id),
        l,
    ]);
});

// Starting point
const AA = relevant_nodes.find((n) => n.id === "AA");

const short_path_solver = new AStarSolver({
    hash: (n) => n.id,
    neighbors: (n) => n.links.map(([a]) => a),
    cost: (src, tgt, c) => src.links.find(([t]) => t.id === tgt.id)[1] + c,
    heuristic: (_, c) => c, // Dijkstra :)
    compareHeuristic: (h1, h2) => h2 - h1, // Smaller is better
});

// Compute shortest path from every meaningful node (flow > 0)
// and starting point to every other meaningful node
const shortest_path = relevant_nodes
    .filter((n) => n.flow > 0)
    .concat(AA)
    .map((n) => ({
        id: n.id,
        links: relevant_nodes
            .filter((t) => t.flow > 0 && t.id !== n.id)
            .map((t) => [
                t.id,
                short_path_solver.solve({
                    start: n,
                    isGoal: (v) => v.id === t.id,
                }).cost,
            ]),
    }));

part_one(walk(AA, 30, new Set(["AA"]))[1]);

const s2 = walk_p2(AA, AA, 26, 26, new Set(["AA"]));
part_two(s2[1] + s2[3]);

function walk(start, duration, avoid) {
    if (duration <= 0) return [[], 0];
    let d0 = start.flow === 0 ? duration : duration - 1;
    let f = start.flow * d0;
    let subtrees = shortest_path
        .find((n) => n.id === start.id)
        .links.filter(([n, d]) => !avoid.has(n) && d0 > d + 1)
        .map(([n, d]) =>
            walk(
                relevant_nodes.find((r) => r.id === n),
                d0 - d,
                new Set([...avoid, n])
            )
        );
    let [path, best] = subtrees.reduce(
        ([p1, b1], [p2, b2]) => (b1 > b2 ? [p1, b1] : [p2, b2]),
        [[], 0]
    );
    return [[start.id, ...path], f + best];
}

function walk_p2(start1, start2, dur1, dur2, avoid) {
    if (dur1 <= 0 || dur2 <= 0) return [[], 0, [], 0];

    // Try moving from start1
    let d1 = start1.flow === 0 ? dur1 : dur1 - 1;
    let f1 = start1.flow * d1;
    let subtrees1 = shortest_path
        .find((n) => n.id === start1.id)
        .links.filter(([n, d]) => !avoid.has(n) && d1 > d + 1)
        .map(([n, d]) =>
            walk_p2(
                relevant_nodes.find((r) => r.id === n),
                start2,
                d1 - d,
                dur2,
                new Set([...avoid, n])
            )
        );

    let [path1a, best1a, path2a, best2a] = subtrees1.reduce(
        ([p1, b1, p2, b2], [p3, b3, p4, b4]) =>
            b1 + b2 > b3 + b4 ? [p1, b1, p2, b2] : [p3, b3, p4, b4],
        [[], 0, [], 0]
    );

    // Or stop in start1 and move from start2
    let [p3, b3] = walk(start2, dur2, avoid);
    if (best1a + best2a > b3) {
        return [[start1.id, ...path1a], best1a + f1, path2a, best2a];
    } else {
        return [[start1.id], f1, p3, b3];
    }
}

function next(src, id, op = 0) {
    const tgt = nodes.find((n) => n.id === id);
    if (tgt.id === "AA" || tgt.flow > 0) return [tgt, op + 1];
    let n = tgt.links
        .map((id) => nodes.find((n) => n.id === id))
        .filter((n) => n.id != src.id);
    if (n.length === 1 && n[0].flow === 0) return next(tgt, n[0].id, op + 1);
    if (n.length === 1) return [n[0], op + 2];
    return n;
}
