const shuffle = require("knuth-shuffle-seeded");
const { range } = require("../common/Collection/util");
const { getNextId, randomInt } = require("../common/Random/util");
const Tree = require("./tree_sorting");

function randomTree(scope, depth, width, maxSortOrder = 10) {
    const children = [...range(depth > 0 ? randomInt(width) : 0)].map(() =>
        randomTree(scope, depth - 1, width)
    );
    let sortOrder = 0;
    children.forEach((child) => {
        sortOrder += randomInt(maxSortOrder) + 1;
        child.sortOrder = sortOrder;
    });
    return new Tree(
        getNextId(scope),
        randomInt(width * maxSortOrder),
        children
    );
}

function TreeInput(name, items, solution) {
    this.name = name;
    this.items = items;
    this.solution = solution;
}

function addHardcodedExample(name, lines) {
    const items = lines.map(([order, parent], idx) => [idx, parent, order]);
    const solution = lines.map(([, , lineNum], idx) => [idx, lineNum]);
    hardcodedExamples.push(new TreeInput(name, items, solution));
}

function generateRandomTrees(nb) {
    return [...range(nb)].map((n) => {
        const scope = `tree-id-${getNextId("tree-scope")}`;
        const lines = randomTree(scope, 4, 13).lines();
        const rootId = lines[0][0];
        const items = shuffle(
            lines
                .slice(1)
                .map(([itemId, parent, sortOrder]) => [
                    itemId,
                    parent === rootId ? null : parent,
                    sortOrder,
                ])
        );
        const solution = lines
            .slice(1)
            .map(([itemId, , , lineNum]) => [itemId, lineNum]);
        return new TreeInput(`gen-tree-${n}`, items, solution);
    });
}

const hardcodedExamples = [];

/* Non hierarchical tests */

addHardcodedExample("empty", []);
addHardcodedExample("single line", [[10, , 1]]);
addHardcodedExample("two ordered lines", [
    [10, , 1],
    [11, , 2],
]);
addHardcodedExample("two shuffled lines", [
    [11, , 2],
    [10, , 1],
]);
addHardcodedExample("4 non hierarchical lines ordered", [
    [10, , 1],
    [11, , 2],
    [12, , 3],
    [13, , 4],
]);
addHardcodedExample("4 non hierarchical lines shuffled inverse order", [
    [14, , 4],
    [13, , 3],
    [12, , 2],
    [11, , 1],
]);
addHardcodedExample("4 non hierarchical lines shuffled", [
    [12, , 3],
    [10, , 1],
    [11, , 2],
    [13, , 4],
]);

/* Hierarchical tests */

addHardcodedExample("parent-child ordered & consistent so", [
    [10, , 1],
    [11, 0, 2],
]);
addHardcodedExample("parent-child ordered & inconsistent so", [
    [11, , 1],
    [10, 0, 2],
]);
addHardcodedExample("parent-child inverted & inconsistent so", [
    [10, 1, 2],
    [11, , 1],
]);
addHardcodedExample("parent-child inverted & consistent so", [
    [11, 1, 2],
    [10, , 1],
]);

addHardcodedExample("4 hierarchical lines shuffled", [
    [12, , 3],
    [10, 2, 2],
    [11, , 1],
    [13, 0, 4],
]);

addHardcodedExample("9 hierarchical lines ordered", [
    [10, , 1],
    [11, 0, 2],
    [12, 0, 3],
    [13, , 4],
    [14, 3, 5],
    [15, 4, 6],
    [16, , 7],
    [17, 6, 8],
    [18, 6, 9],
]);

addHardcodedExample("9 hierarchical lines shuffled & consistent sort order", [
    [17, 4, 8],
    [10, , 1],
    [15, 6, 6],
    [12, 1, 3],
    [16, , 7],
    [11, 1, 2],
    [14, 8, 5],
    [18, 4, 9],
    [13, , 4],
]);

addHardcodedExample("9 hierarchical lines shuffled & inconsistent so", [
    [31, 4, 8],
    [30, , 1],
    [12, 6, 6],
    [35, 1, 3],
    [37, , 7],
    [17, 1, 2],
    [66, 8, 5],
    [44, 4, 9],
    [34, , 4],
]);

addHardcodedExample("9 hierarchical lines shuffled & duplicate so", [
    [20, 4, 8],
    [10, , 1],
    [20, 6, 6],
    [20, 1, 3],
    [30, , 7],
    [10, 1, 2],
    [20, 8, 5],
    [30, 4, 9],
    [20, , 4],
]);

const generatedExamples = generateRandomTrees(20);

module.exports = {
    hardcodedExamples,
    generatedExamples,
};
