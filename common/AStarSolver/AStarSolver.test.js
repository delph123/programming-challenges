const AStarSolver = require("./AStarSolver");

const grid = [
    ["A", "B", 85],
    ["A", "C", 217],
    ["A", "E", 173],
    ["B", "F", 80],
    ["C", "G", 186],
    ["C", "H", 103],
    ["H", "D", 183],
    ["F", "I", 250],
    ["I", "J", 84],
    ["E", "J", 502],
    ["H", "J", 167],
];

const estimations = new Map([
    ["A", 450],
    ["B", 380],
    ["C", 240],
    ["D", 320],
    ["E", 500],
    ["F", 330],
    ["G", 200],
    ["H", 165],
    ["I", 80],
    ["J", 0],
]);

function edges(from) {
    const one = grid.filter(([s]) => s === from);
    const two = grid
        .filter(([s, e]) => e === from)
        .map(([s, e, c, h]) => [e, s, c, h]);
    return one.concat(two);
}

test("Dijkstra Solver (estimation = 0)", () => {
    solver = new AStarSolver({
        hash: (node) => node,
        neighbours: (node) => edges(node).map(([, t]) => t),
        cost: (from, to, cost) =>
            cost + edges(from).filter(([, t]) => t === to)[0][2],
        heuristic: (_, cost) => cost,
        compareHeuristic: (a, b) => b - a,
    });

    let { path, cost, visited } = solver.solve({
        start: "A",
        isGoal: (node) => node === "J",
    });

    expect(path.join("")).toEqual("ACHJ");
    expect(cost).toEqual(487);
    expect(visited).toEqual(8);

    ({ path, cost, visited } = solver.solve({
        start: "E",
        isGoal: (node) => node === "D",
    }));

    expect(path.join("")).toEqual("EACHD");
    expect(cost).toEqual(676);
    expect(visited).toEqual(9);

    ({ path, cost, visited } = solver.solve({
        start: "G",
        isGoal: (node) => node === "I",
    }));

    expect(path.join("")).toEqual("GCHJI");
    expect(cost).toEqual(540);
    expect(visited).toEqual(7);

    expect(
        solver.solve.bind(solver, {
            start: "G",
            isGoal: (node) => node === "K",
        })
    ).toThrow();
});

test("A* Solver", () => {
    const solver = new AStarSolver({
        hash: (node) => node,
        neighbours: (node) => edges(node).map(([, t]) => t),
        cost: (from, to, cost) =>
            cost + edges(from).filter(([, t]) => t === to)[0][2],
        heuristic: (node, cost) => cost + estimations.get(node),
        compareHeuristic: (a, b) => b - a,
        start: "A",
        isGoal: (node) => node === "J",
    });

    const { path, cost, visited } = solver.solve();

    expect(path.join("")).toEqual("ACHJ");
    expect(cost).toEqual(487);
    expect(visited).toEqual(4);
});
