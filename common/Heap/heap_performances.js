const Heap = require("./BinaryMaxHeap");
const Heap2 = require("./Heap");

function generateRecords(size) {
    return new Array(size).fill(0).map(() => Math.random());
}

function equalsKey(a, b) {
    return Object.equal(a.key, b.key);
}
function compareKeys(a, b) {
    return b.key - a.key;
}
function toKey(n) {
    return { key: n };
}

function buildHeap(recs, recs2, name, listner) {
    console.time("build-" + name);
    let h = new Heap(recs, compareKeys, listner);
    console.timeEnd("build-" + name);
    console.time("concat-" + name);
    h.addEach(recs2);
    console.timeEnd("concat-" + name);
    console.time("push-" + name);
    h.push(...[5, -4, 2, 0, 8].map(toKey));
    console.timeEnd("push-" + name);
    console.time("clone-" + name);
    const c = h.clone();
    console.timeEnd("clone-" + name);
    console.time("merge-" + name);
    h.merge(c);
    console.timeEnd("merge-" + name);
    console.time("pop-" + name);
    while (h.length > 0) {
        h.pop();
    }
    console.timeEnd("pop-" + name);
}

function buildHeap2(recs, recs2, name, listner) {
    console.time("build-" + name);
    let h = new Heap2(recs, equalsKey, compareKeys);
    if (listner) {
        h.addMapChangeListener(listner);
    }
    console.timeEnd("build-" + name);
    console.time("concat-" + name);
    h.addEach(recs2);
    console.timeEnd("concat-" + name);
    console.time("push-" + name);
    h.push(...[5, -4, 2, 0, 8].map(toKey));
    console.timeEnd("push-" + name);
    console.time("clone-" + name);
    const c = h.clone();
    console.timeEnd("clone-" + name);
    console.time("merge-" + name);
    h.merge(c);
    console.timeEnd("merge-" + name);
    console.time("pop-" + name);
    while (h.length > 0) {
        h.pop();
    }
    console.timeEnd("pop-" + name);
}

function buildArray(recs, recs2, name) {
    let h = [];
    console.time("build-" + name);
    recs.forEach((r) => {
        h.push(r);
    });
    console.timeEnd("build-" + name);
    console.time("concat-" + name);
    recs2.forEach((r) => {
        h.push(r);
    });
    console.timeEnd("concat-" + name);
    console.time("push-" + name);
    h.push(...[5, -4, 2, 0, 8].map(toKey));
    console.timeEnd("push-" + name);
    console.time("clone-" + name);
    const c = h.slice();
    console.timeEnd("clone-" + name);
    console.time("merge-" + name);
    h = h.concat(c);
    console.timeEnd("merge-" + name);
    console.time("pop-" + name);
    while (h.length > 0) {
        h.pop();
    }
    console.timeEnd("pop-" + name);
}

console.log("--");

console.time("generate");
const recs = generateRecords(1_000_000).map(toKey);
const recs2 = generateRecords(1_000_000).map(toKey);
console.timeEnd("generate");

console.log("--");

console.time("array");
buildArray(recs, recs2, "array");
console.timeEnd("array");

console.log("--");

console.time("naked-heap");
buildHeap(recs, recs2, "naked-heap", undefined);
console.timeEnd("naked-heap");

console.log("--");

console.time("monitored-heap");
buildHeap(recs, recs2, "monitored-heap", (value, index) => {
    // The map change listner keeps the idx attribute
    // equal to the actual index in the heap!
    value.idx = index;
});
console.timeEnd("monitored-heap");

console.log("--");

console.time("collections-heap");
buildHeap2(recs, recs2, "collections-heap", undefined);
console.timeEnd("collections-heap");

console.log("--");

// console.time("collections-monitored-heap");
// buildHeap2(recs, recs2, "collections-monitored-heap", (value, index) => {
//     if (value !== undefined) {
//         // The map change listner keeps the idx attribute
//         // equal to the actual index in the heap!
//         value.idx = index;
//     }
// });
// console.timeEnd("collections-monitored-heap");

// console.log("--");
