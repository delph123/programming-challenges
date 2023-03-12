const { zip, zipLongest, range, expand, collect } = require("./util");

describe("zip", () => {
    it("Returns nothing for no input", () => {
        expect([...zip()]).toEqual([]);
    });

    it("Returns same array wrapped for single iterable input", () => {
        expect([...zip([])]).toEqual([]);
        expect([...zip([1])]).toEqual([[1]]);
        expect([...zip([1, 2, 3])]).toEqual([[1], [2], [3]]);
    });

    it("Returns zip of 2 iterables of same length", () => {
        expect([...zip([], [])]).toEqual([]);
        expect([...zip([1], [6])]).toEqual([[1, 6]]);
        expect([...zip([1, 2, 3], [6, 5, 4])]).toEqual([
            [1, 6],
            [2, 5],
            [3, 4],
        ]);
    });

    it("Stops at smallest iterable", () => {
        expect([...zip([], [5, 6, 7])]).toEqual([]);
        expect([...zip([1], [6, 5, 4])]).toEqual([[1, 6]]);
        expect([...zip([1, 2, 3, 4, 5, 6], [6, 5, 4])]).toEqual([
            [1, 6],
            [2, 5],
            [3, 4],
        ]);
    });

    it("Returns zip of 4 iterables", () => {
        expect([...zip([], [], [], [])]).toEqual([]);
        expect([...zip([1], [6], ["a"], [false])]).toEqual([
            [1, 6, "a", false],
        ]);
        expect([
            ...zip([1, 2, 3], [6, 5, 4], ["b", "c", "d"], [true, false, true]),
        ]).toEqual([
            [1, 6, "b", true],
            [2, 5, "c", false],
            [3, 4, "d", true],
        ]);
    });

    it("Accepts different kind of iterables", () => {
        function* gen(input) {
            for (let value of input) {
                yield value;
            }
        }

        expect([...zip([], new Set(), "", gen([]))]).toEqual([]);
        expect([...zip([1], new Set([6]), "a", gen([false]))]).toEqual([
            [1, 6, "a", false],
        ]);
        expect([
            ...zip(
                [1, 2, 3],
                new Set([6, 5, 4]),
                "bcd",
                gen([true, false, true])
            ),
        ]).toEqual([
            [1, 6, "b", true],
            [2, 5, "c", false],
            [3, 4, "d", true],
        ]);
    });
});

describe("zipLongest", () => {
    it("Returns nothing for no input", () => {
        expect([...zipLongest()]).toEqual([]);
    });

    it("Returns same array wrapped for single iterable input", () => {
        expect([...zipLongest([])]).toEqual([]);
        expect([...zipLongest([1])]).toEqual([[1]]);
        expect([...zipLongest([1, 2, 3])]).toEqual([[1], [2], [3]]);
    });

    it("Returns zip of 2 iterables of same length", () => {
        expect([...zipLongest([], [])]).toEqual([]);
        expect([...zipLongest([1], [6])]).toEqual([[1, 6]]);
        expect([...zipLongest([1, 2, 3], [6, 5, 4])]).toEqual([
            [1, 6],
            [2, 5],
            [3, 4],
        ]);
    });

    it("Iterates to longest iterable", () => {
        expect([...zipLongest([], [5, 6, 7])]).toEqual([
            [undefined, 5],
            [undefined, 6],
            [undefined, 7],
        ]);
        expect([...zipLongest([1], [6, 5, 4])]).toEqual([
            [1, 6],
            [undefined, 5],
            [undefined, 4],
        ]);
        expect([...zipLongest([1, 2, 3, 4, 5, 6], [6, 5, 4])]).toEqual([
            [1, 6],
            [2, 5],
            [3, 4],
            [4, undefined],
            [5, undefined],
            [6, undefined],
        ]);
    });

    it("Fills missing values of short iterables with fillValue", () => {
        expect([...zipLongest([], [], [], 0)]).toEqual([]);
        expect([...zipLongest([1], [true, false], ["a"], 0)]).toEqual([
            [1, true, "a"],
            [0, false, 0],
        ]);
        expect([
            ...zipLongest([1, 2, 3, 4], [6, 5], ["b", "c", "d", "e", "f"], 0),
        ]).toEqual([
            [1, 6, "b"],
            [2, 5, "c"],
            [3, 0, "d"],
            [4, 0, "e"],
            [0, 0, "f"],
        ]);
    });

    it("Accepts different kind of iterables", () => {
        function* gen(input) {
            for (let value of input) {
                yield value;
            }
        }

        expect([...zipLongest([], new Set(), "", gen([]))]).toEqual([]);
        expect([...zipLongest([1], new Set([6]), "a", gen([false]))]).toEqual([
            [1, 6, "a", false],
        ]);
        expect([
            ...zipLongest(
                [1, 2, 3],
                new Set([6, 5, 4]),
                "bcd",
                gen([true, false, true])
            ),
        ]).toEqual([
            [1, 6, "b", true],
            [2, 5, "c", false],
            [3, 4, "d", true],
        ]);
    });
});

describe("Range", () => {
    it("Creates a range of 0..n", () => {
        expect([...range(0)]).toEqual([]);
        expect([...range(4)]).toEqual([0, 1, 2, 3]);
    });

    it("Creates a range of s..e", () => {
        expect(collect([range(0, 0)])).toEqual([]);
        expect(collect([range(2, 4)])).toEqual([2, 3]);
    });

    it("Creates a range of s..e with step 5", () => {
        expect(expand(range(0, -2, 5))).toEqual([]);
        expect(expand(range(2, 30, 5))).toEqual([2, 7, 12, 17, 22, 27]);
    });

    it("Creates a range of s..e with step -1", () => {
        expect(Array.from(range(0, 0, -1))).toEqual([]);
        expect(Array.from(range(2, -4, -1))).toEqual([2, 1, 0, -1, -2, -3]);
    });
});
