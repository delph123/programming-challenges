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

it("It creates a max heap from a list", () => {
    const h = new Heap([4, 3, 5, 8, 2, 1]);
    expect(h.length).toBe(6);
    expect(extractsAllInOrder(h)).toEqual([8, 5, 4, 3, 2, 1]);
});

test("It adds mutiple elements to a max heap from a list in bulk", () => {
    const h = new Heap([4, 3]);
    h.addEach([5, 8, 2, 1]);
    expect(h.length).toBe(6);
    expect(extractsAllInOrder(h)).toEqual([8, 5, 4, 3, 2, 1]);
});

test("It adds mutiple elements to a max heap from a list one by one", () => {
    const h = new Heap([4, 3, 5, 8, 2, 1, 12]);
    h.addEach([6, 15, 3]);
    expect(h.length).toBe(10);
    expect(extractsAllInOrder(h)).toEqual([15, 12, 8, 6, 5, 4, 3, 3, 2, 1]);
});

test("It pushes elements to a max heap from a list in bulk", () => {
    const h = new Heap([4, 3]);
    h.push(5, 8, 2, 1);
    expect(h.length).toBe(6);
    expect(extractsAllInOrder(h)).toEqual([8, 5, 4, 3, 2, 1]);
});

test("It pushes elements to a max heap from a list one by one", () => {
    const h = new Heap([4, 3, 5, 8, 2, 1, 12]);
    h.push(6, 15, 3);
    expect(h.length).toBe(10);
    expect(extractsAllInOrder(h)).toEqual([15, 12, 8, 6, 5, 4, 3, 3, 2, 1]);
});

test("It adds a single element to a max heap", () => {
    const h = new Heap([4, 3, 5, 8, 2, 1, 12]);
    h.add(28);
    expect(h.length).toBe(8);
    expect(extractsAllInOrder(h)).toEqual([28, 12, 8, 5, 4, 3, 2, 1]);
});

test("It pushes a single elements to a max heap", () => {
    const h = new Heap([4, 3, 5, 8, 2, 1, 12]);
    h.push(6);
    expect(h.length).toBe(8);
    expect(extractsAllInOrder(h)).toEqual([12, 8, 6, 5, 4, 3, 2, 1]);
});

test("It concatenates a max heap with a list", () => {
    const h = new Heap([4, 8, 2, 6, 12]);
    const v = h.concat([5, 7, 9], [6, 0]);
    expect(extractsAllInOrder(h)).toEqual([12, 8, 6, 4, 2]);
    expect(extractsAllInOrder(v)).toEqual([12, 9, 8, 7, 6, 6, 5, 4, 2, 0]);
});

test("It accepts a change listner", () => {
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

test("It can be reversed in place", () => {
    const h = new Heap([4, 8, 2, 6, 12]);
    const expected = [12, 8, 6, 4, 2];
    expect(extractsAllInOrder(h.clone())).toEqual(expected);
    h.reverse();
    expect(extractsAllInOrder(h.clone())).toEqual(expected.slice().reverse());
    h.reverse();
    expect(extractsAllInOrder(h.clone())).toEqual(expected);
});

test("It can be reversed without impact", () => {
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
