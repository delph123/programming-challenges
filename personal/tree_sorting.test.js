const { hardcodedExamples, generatedExamples } = require("./trees_input");
const Tree = require("./tree_sorting");

function testInput(treeFromInput, input) {
    test(`${input.name} with ${input.items.length} lines`, () => {
        const lines = treeFromInput(input.items)
            .lines()
            .slice(1)
            .map(([itemId, , , lineNum]) => [itemId, lineNum]);
        expect(new Map(lines)).toEqual(new Map(input.solution));
    });
}

describe("Check line number hardcoded", () => {
    hardcodedExamples.forEach((input) => testInput((l) => Tree.from(l), input));
});

describe("Check line number generated", () => {
    generatedExamples.forEach((input) => testInput((l) => Tree.from(l), input));
});

describe("Check line number hardcoded with O(n^2) parser", () => {
    hardcodedExamples.forEach((input) =>
        testInput((l) => Tree.from_quadratic(l).sort(), input)
    );
});

describe("Check line number generated with O(n^2) parser", () => {
    generatedExamples.forEach((input) =>
        testInput((l) => Tree.from_quadratic(l).sort(), input)
    );
});
