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

const [vertices, distances, flows] = shortest_dist();
const avoid = new Array(vertices.length).fill(false).map((_, i) => i === 0);

const paths_30 = paths_arrangements(0, 30, avoid);
part_one(paths_30.reduce((a, b) => (a[1] > b[1] ? a : b), [[], 0])[1]);

part_two(joined_paths(0, 26, avoid));

function joined_paths(start, duration, avoid) {
    const sub_paths = paths_arrangements(start, duration, avoid);
    const best_avoiding = new Map();
    let max = 0;
    for (let i = 0; i < sub_paths.length; i++) {
        const path = toKey(sub_paths[i][0].slice(1));
        if (!best_avoiding.has(path)) {
            let bmax = 0;
            const avoid = new Set(sub_paths[i][0].slice(1));
            // There is no need to loop again over paths we've already
            // explored. Those will always be taken into account in current
            // max. We can start from position i+1
            for (let j = i + 1; j < sub_paths.length; j++) {
                // Exclude paths with intersecting nodes (both players
                // should not open the same valve)
                if (sub_paths[j][0].every((v) => !avoid.has(v))) {
                    bmax = Math.max(bmax, sub_paths[j][1]);
                }
            }
            best_avoiding.set(path, bmax);
        }
        max = Math.max(max, sub_paths[i][1] + best_avoiding.get(path));
    }
    return max;
}

function toKey(indices) {
    // Compute a unique key representing traversed vertices
    // (unique in such a way that two paths traversing the same
    // vertices in a different order will have the same key)
    const vert = new Array(vertices.length).fill(0);
    for (let i of indices) {
        vert[i] = 1;
    }
    return vert.join(""); // convert to string to be usable as Map key
}

function paths_arrangements(start, duration, avoided) {
    // First arrangement: do nothing
    const paths = [[[start], 0]];
    // Check other paths so long that we have enough duration to
    // open the next valve and that the valve is not already opened
    for (let i = 0; i < vertices.length; i++) {
        if (!avoided[i] && distances[start][i] + 1 < duration) {
            avoided[i] = true;
            const sub = paths_arrangements(
                i,
                duration - distances[start][i] - 1,
                avoided
            );
            for (const [p, f] of sub) {
                paths.push([
                    [start, ...p],
                    flows[i] * (duration - distances[start][i] - 1) + f,
                ]);
            }
            avoided[i] = false;
        }
    }
    return paths;
}

function shortest_dist() {
    let vertices = nodes
        .filter((n) => n.id !== "AA")
        .sort((n1, n2) => n1.flow - n2.flow)
        .concat(nodes.find((n) => n.id === "AA"))
        .reverse();

    // Compute shortest distance between all nodes with Floyd–Warshall algorithm
    let dist = new Array(vertices.length)
        .fill(0)
        .map(() => new Array(vertices.length).fill(Infinity));

    vertices.forEach((v, i) => {
        dist[i][i] = 0;
        v.links.forEach((dest) => {
            dist[i][vertices.findIndex((n) => n.id === dest)] = 1;
        });
    });

    for (let k = 0; k < vertices.length; k++) {
        for (let i = 0; i < vertices.length; i++) {
            for (let j = 0; j < vertices.length; j++) {
                dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
            }
        }
    }

    // Now, keep only meaningful nodes (starting point and nodes with flow > 0)
    const flows = vertices
        .filter((nd) => nd.id === "AA" || nd.flow > 0)
        .map((nd) => nd.flow);

    vertices = vertices
        .filter((nd) => nd.id === "AA" || nd.flow > 0)
        .map((nd) => nd.id);

    dist = dist
        .map((nodes) => nodes.slice(0, vertices.length))
        .slice(0, vertices.length);

    return [vertices, dist, flows];
}
