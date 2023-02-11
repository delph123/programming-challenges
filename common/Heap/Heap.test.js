const Heap = require("./Heap");

function extractsAllInOrder(heap) {
    const result = [];
    while (heap.length > 0) {
        result.push(heap.pop());
    }
    return result;
}

test("It creates a max heap from a list", () => {
    const h = new Heap([4, 3, 5, 8, 2, 1]);
    expect(h.length).toBe(6);
    expect(extractsAllInOrder(h)).toEqual([8, 5, 4, 3, 2, 1]);
})

test("It adds mutiple elements to a max heap from a list in bulk", () => {
    const h = new Heap([4, 3]);
    h.addEach([5, 8, 2, 1]);
    expect(h.length).toBe(6);
    expect(extractsAllInOrder(h)).toEqual([8, 5, 4, 3, 2, 1]);
})

test("It adds mutiple elements to a max heap from a list one by one", () => {
    const h = new Heap([4, 3, 5, 8, 2, 1, 12]);
    h.addEach([6, 15, 3]);
    expect(h.length).toBe(10);
    expect(extractsAllInOrder(h)).toEqual([15, 12, 8, 6, 5, 4, 3, 3, 2, 1]);
})

test("It pushes elements to a max heap from a list in bulk", () => {
    const h = new Heap([4, 3]);
    h.push(5, 8, 2, 1);
    expect(h.length).toBe(6);
    expect(extractsAllInOrder(h)).toEqual([8, 5, 4, 3, 2, 1]);
})

test("It pushes elements to a max heap from a list one by one", () => {
    const h = new Heap([4, 3, 5, 8, 2, 1, 12]);
    h.push(6, 15, 3);
    expect(h.length).toBe(10);
    expect(extractsAllInOrder(h)).toEqual([15, 12, 8, 6, 5, 4, 3, 3, 2, 1]);
})

test("It adds a single element to a max heap", () => {
    const h = new Heap([4, 3, 5, 8, 2, 1, 12]);
    h.add(28);
    expect(h.length).toBe(8);
    expect(extractsAllInOrder(h)).toEqual([28, 12, 8, 5, 4, 3, 2, 1]);
})

test("It pushes a single elements to a max heap", () => {
    const h = new Heap([4, 3, 5, 8, 2, 1, 12]);
    h.push(6);
    expect(h.length).toBe(8);
    expect(extractsAllInOrder(h)).toEqual([12, 8, 6, 5, 4, 3, 2, 1]);
})