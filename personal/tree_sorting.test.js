const { hardcodedExamples, generatedExamples } = require("./trees_input");
const Tree = require("./tree_sorting");

function testInput(input) {
    test(input.name, () => {
        const lines = Tree.from(input.items)
            .lines()
            .slice(1)
            .map(([itemId, , , lineNum]) => [itemId, lineNum]);
        expect(new Map(lines)).toEqual(new Map(input.solution));
    });
}

describe("Check line number hardcoded", () => {
    hardcodedExamples.forEach(testInput);
});

describe("Check line number generated", () => {
    generatedExamples.forEach(testInput);
});
