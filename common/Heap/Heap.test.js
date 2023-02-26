const Heap = require("./BinaryMaxHeap");

function range(n) {
    return new Array(n).fill(0).map((_, i) => i);
}

function extractsAllInOrder(heap) {
    const result = [];
    while (heap.length > 0) {
        result.push(heap.pop());
    }
    return result;
}

describe("Heap creation", () => {
    it("Create an empty heap", () => {
        expect(new Heap().length).toEqual(0);
        expect(new Heap().content).toEqual([]);
        expect(new Heap([]).length).toEqual(0);
        expect(new Heap([]).content).toEqual([]);
    });

    it("Creates a max heap from an array", () => {
        const h = new Heap([4, 3, 5, 8, 2, 1]);
        expect(h.length).toBe(6);
        expect(extractsAllInOrder(h)).toEqual([8, 5, 4, 3, 2, 1]);
    });

    it("Creates a max heap from an iterable", () => {
        const h = new Heap(new Set([1, 2, 3]));
        expect(h.length).toBe(3);
        expect(extractsAllInOrder(h)).toEqual([3, 2, 1]);
    });

    it("Creates a max heap from an iterator", () => {
        const h = new Heap(new Set([1, 2, 3])[Symbol.iterator]());
        expect(h.length).toBe(3);
        expect(extractsAllInOrder(h)).toEqual([3, 2, 1]);
    });

    it("Creates a max heap from a generator", () => {
        function* gen() {
            yield 1;
            yield 2;
            yield 3;
        }
        const h = new Heap(gen());
        expect(h.length).toBe(3);
        expect(extractsAllInOrder(h)).toEqual([3, 2, 1]);
    });

    it("Creates a max heap from an array-like", () => {
        function createHeap() {
            return new Heap(arguments);
        }
        const h = createHeap(4, 3, 5, 8, 2, 1);
        expect(h.length).toBe(6);
        expect(extractsAllInOrder(h)).toEqual([8, 5, 4, 3, 2, 1]);
    });

    it("Creates a max heap from an object with length", () => {
        const h = new Heap({ ...[4, 3, 5, 8, 2, 1], length: 6 });
        expect(h.length).toBe(6);
        expect(extractsAllInOrder(h)).toEqual([8, 5, 4, 3, 2, 1]);
    });

    it("Creates a min heap by providing a compare function", () => {
        const h = new Heap([1, 2, 3, 6, 9, 4, 0], (a, b) => b - a);
        expect(extractsAllInOrder(h)).toEqual([0, 1, 2, 3, 4, 6, 9]);
    });
});

describe("Heap modifications", () => {
    it("Adds mutiple elements to a max heap from a list in bulk", () => {
        const h = new Heap([4, 3]);
        h.addEach([5, 8, 2, 1]);
        expect(h.length).toBe(6);
        expect(extractsAllInOrder(h)).toEqual([8, 5, 4, 3, 2, 1]);
    });

    it("Adds mutiple elements to a max heap from a list one by one", () => {
        const h = new Heap([4, 3, 5, 8, 2, 1, 12]);
        h.addEach([6, 15, 3]);
        expect(h.length).toBe(10);
        expect(extractsAllInOrder(h)).toEqual([15, 12, 8, 6, 5, 4, 3, 3, 2, 1]);
    });

    it("Pushes elements to a max heap from a list in bulk", () => {
        const h = new Heap([4, 3]);
        h.push(5, 8, 2, 1);
        expect(h.length).toBe(6);
        expect(extractsAllInOrder(h)).toEqual([8, 5, 4, 3, 2, 1]);
    });

    it("Pushes elements to a max heap from a list one by one", () => {
        const h = new Heap([4, 3, 5, 8, 2, 1, 12]);
        h.push(6, 15, 3);
        expect(h.length).toBe(10);
        expect(extractsAllInOrder(h)).toEqual([15, 12, 8, 6, 5, 4, 3, 3, 2, 1]);
    });

    it("Adds a single element to a max heap", () => {
        const h = new Heap([4, 3, 5, 8, 2, 1, 12]);
        h.add(28);
        expect(h.length).toBe(8);
        expect(extractsAllInOrder(h)).toEqual([28, 12, 8, 5, 4, 3, 2, 1]);
    });

    it("Pushes a single elements to a max heap", () => {
        const h = new Heap([4, 3, 5, 8, 2, 1, 12]);
        h.push(6);
        expect(h.length).toBe(8);
        expect(extractsAllInOrder(h)).toEqual([12, 8, 6, 5, 4, 3, 2, 1]);
    });

    it("Concatenates a max heap with a list", () => {
        const h = new Heap([4, 8, 2, 6, 12]);
        const v = h.concat(new Set([5, 7]), [9], new Heap([6, 0]));
        expect(extractsAllInOrder(h)).toEqual([12, 8, 6, 4, 2]);
        expect(extractsAllInOrder(v)).toEqual([12, 9, 8, 7, 6, 6, 5, 4, 2, 0]);
    });

    it("Clears its content", () => {
        const h = new Heap([4, 8, 2, 6, 12]);
        h.clear();
        expect(h.length).toBe(0);
        expect(h.content).toEqual([]);
        expect(h.pop()).toEqual(undefined);
        expect(h.length).toBe(0);
    });
});

describe("Change Listner", () => {
    it("Accepts a change listner", () => {
        function compareKeys(a, b) {
            return a.key - b.key;
        }
        const h = new Heap([], compareKeys, (value, index) => {
            if (value !== undefined) {
                // The map change listner keeps the idx attribute
                // equal to the actual index in the heap!
                value.idx = index;
            }
        });

        h.addEach([{ key: 6 }, { key: 12 }, { key: 7 }, { key: 17 }]);
        // Therefore elements index shall be 0 .. n
        expect(h.map((v) => v.idx)).toEqual(range(h.length));
        h.add({ key: 21 });
        expect(h.map((v) => v.idx)).toEqual(range(h.length));
        h.pop();
        expect(h.map((v) => v.idx)).toEqual(range(h.length));
        h.push({ key: 3 }, { key: 16 }, { key: 8 });
        expect(h.map((v) => v.idx)).toEqual(range(h.length));
    });
});

describe("Other APIs", () => {
    it("Can be reversed in place", () => {
        const h = new Heap([4, 8, 2, 6, 12]);
        const expected = [12, 8, 6, 4, 2];
        expect(extractsAllInOrder(h.clone())).toEqual(expected);
        h.reverse();
        expect(extractsAllInOrder(h.clone())).toEqual(
            expected.slice().reverse()
        );
        h.reverse();
        expect(extractsAllInOrder(h.clone())).toEqual(expected);
    });

    it("Can be reversed without impact", () => {
        function compareKeys(a, b) {
            return b.key - a.key;
        }
        function toKey(n) {
            return { key: n };
        }
        // This is a min-heap due to comparison function
        const h = new Heap([4, 8, 2, 6, 12].map(toKey), compareKeys);
        const expected = [2, 4, 6, 8, 12].map(toKey);
        expect(extractsAllInOrder(h.reversed())).toEqual(
            expected.slice().reverse()
        );
        expect(extractsAllInOrder(h.clone())).toEqual(expected);
    });
});
