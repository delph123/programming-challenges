const Heap = require("../Heap");

class AStarSolver {
    getHash;
    getNeighbors;
    cost;
    heuristic;
    compareHeuristic;

    startingPoint;
    isGoal;

    constructor({
        hash,
        neighbors,
        cost,
        heuristic,
        compareHeuristic,
        start,
        isGoal,
    }) {
        this.getHash = hash;
        this.getNeighbors = neighbors;
        this.cost = cost;
        this.heuristic = heuristic;
        this.compareHeuristic = compareHeuristic;

        if (Boolean(start)) {
            this.startingPoint = this.mapToAStarNode(start, null);
        }
        if (Boolean(isGoal)) {
            this.isGoal = isGoal;
        }
    }

    solve({ start, isGoal } = {}) {
        if (Boolean(start)) {
            this.startingPoint = this.mapToAStarNode(start, null);
        }
        if (Boolean(isGoal)) {
            this.isGoal = isGoal;
        }

        const visited = new Map();
        const candidates = new Heap(
            [this.startingPoint],
            (a, b) => this.compareHeuristic(a.heuristic, b.heuristic),
            (value, index) => {
                value.index = index;
            }
        );
        const nodesMap = new Map([
            [this.startingPoint.hash, this.startingPoint],
        ]);

        while (candidates.length > 0) {
            const bestCandidate = candidates.pop();

            if (this.isGoal(bestCandidate.node)) {
                return this.reconstructPath(bestCandidate, visited);
            }

            const neighbors = this.getNeighbors(bestCandidate.node)
                .map((n) => this.mapToAStarNode(n, bestCandidate))
                .filter((n) => !visited.has(n.hash));

            neighbors.forEach((n) => {
                if (nodesMap.has(n.hash)) {
                    let node = nodesMap.get(n.hash);
                    if (
                        this.compareHeuristic(n.heuristic, node.heuristic) > 0
                    ) {
                        node.cost = n.cost;
                        node.heuristic = n.heuristic;
                        node.predecessor = n.predecessor;
                        candidates.heapifyUp(node.index);
                    }
                } else {
                    candidates.push(n);
                    nodesMap.set(n.hash, n);
                }
            });

            visited.set(bestCandidate.hash, bestCandidate);
        }

        throw new Error(
            "Couldn't find a path to goal from this starting point."
        );
    }

    mapToAStarNode(neighbor, predecessor) {
        const neighborCost =
            predecessor == null
                ? 0
                : this.cost(predecessor.node, neighbor, predecessor.cost);
        return {
            node: neighbor,
            hash: this.getHash(neighbor),
            cost: neighborCost,
            heuristic: this.heuristic(neighbor, neighborCost),
            predecessor: predecessor?.hash,
        };
    }

    reconstructPath(goalNode, visited) {
        const path = [goalNode.node];
        let node = goalNode;
        while (node.predecessor != null) {
            node = visited.get(node.predecessor);
            path.push(node.node);
        }
        return {
            path: path.reverse(),
            cost: goalNode.cost,
            visited: visited.size,
        };
    }
}

module.exports = AStarSolver;
