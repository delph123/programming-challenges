const { part_one, part_two, sum, readLines } = require("../../common/aoc");

const treeMap = readLines("i").map((s) => [...s].map((i) => parseInt(i)));

part_one(
    sum(
        treeMap
            .map((trees, i, grid) =>
                trees.map((t, j) => isVisible(grid, i, j, t))
            )
            .map((l) => l.filter((a) => a).length)
    )
);

part_two(
    Math.max(
        ...treeMap
            .map((trees, i, grid) =>
                trees.map((t, j) => scenicScore(grid, i, j, t))
            )
            .flat()
    )
);

function isVisible(grid, i, j, t) {
    if (
        i === 0 ||
        i === grid.length - 1 ||
        j === 0 ||
        j === grid[0].length - 1
    ) {
        return true;
    } else {
        let top = new Array(i).fill(-1).map((_, k) => grid[k][j]);
        let bottom = new Array(grid.length - i - 1)
            .fill(-1)
            .map((_, k) => grid[i + 1 + k][j]);
        return (
            !grid[i].slice(0, j).some((n) => n >= t) ||
            !grid[i].slice(j + 1).some((n) => n >= t) ||
            !top.some((n) => n >= t) ||
            !bottom.some((n) => n >= t)
        );
    }
}

function scenicScore(grid, i, j, t) {
    if (
        i === 0 ||
        i === grid.length - 1 ||
        j === 0 ||
        j === grid[0].length - 1
    ) {
        return 0;
    } else {
        let top = new Array(i).fill(-1).map((_, k) => grid[i - k - 1][j]);
        let bottom = new Array(grid.length - i - 1)
            .fill(-1)
            .map((_, k) => grid[i + 1 + k][j]);
        let left = grid[i].slice(0, j).reverse();
        let right = grid[i].slice(j + 1);
        return (
            viewingDistance(left, t) *
            viewingDistance(right, t) *
            viewingDistance(top, t) *
            viewingDistance(bottom, t)
        );
    }
}

function viewingDistance(arr, t) {
    let vd = arr.findIndex((n) => n >= t);
    return vd < 0 ? arr.length : vd + 1;
}
