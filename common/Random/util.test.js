const { range } = require("../Collection/util");
const { randomInt, getNextId } = require("./util");

describe("randomInt generates an integer between 0 and N-1", () => {
    test.each([1, 2, 10, 874, 1_765_543])(
        "For N = %s, 0 <= randomInt(N) < N",
        (max) => {
            const randNums = [...range(10000)].map(() => randomInt(max));
            randNums.forEach((n) => {
                expect(n).toBeGreaterThanOrEqual(0);
                expect(n).toBeLessThan(max);
                expect(Math.trunc(n)).toEqual(n);
            });
        }
    );
    test.each([1, 2, 10, 874])(
        "Generate all possible numbers between 0 & %s",
        (max) => {
            const randNums = [...range(10000)].map(() => randomInt(max));
            [...range(max)].forEach((n) => {
                expect(randNums).toContain(n);
            });
        }
    );
});

describe("Generate unique IDs", () => {
    test.each([10, 123, 3476])("Generate ID between 0 & %s", (max) => {
        const scope = randomInt(12343);
        const ids = [];
        [...range(max / 3)].forEach(() => {
            const id = getNextId(`scope-${scope}`, max);
            expect(ids).not.toContain(id);
            ids.push(id);
        });
    });
});
