const Heap = require("collections/heap");

const _addEach = Heap.prototype.addEach;

Heap.prototype.merge = function merge(values) {
    let n = this.content.length;
    let k = values.length;

    this.content.push(...values);
    this.length += values.length;

    console.log("Merging", n, "elements with", k, "elements.")

    if (k * Math.log2(n+k) > n + k) {
        console.log("Using Floyd heapify algorithm. Since", k * Math.log2(n+k), ">", n + k);
        let m = Math.trunc(this.length / 2) - 1;
        for (let i = m; i >= 0; i--) {
            this.sink(i);
        }
    } else {
        console.log("Adding elements one by one. Since", k * Math.log2(n+k), "<=", n + k);
        for (let i = n; i < this.content.length; i++) {
            this.float(i);
        }
    }
}

Heap.prototype.addEach = function addEach(values, mapFn, thisp) {
    console.log("Adding each:", values, mapFn, thisp);
    let newValues = [];
    this.add = function add(value) {
        newValues.push(value);
    };
    _addEach.call(this, values, mapFn, thisp);
    delete this.add;
    this.merge(newValues);
}

Heap.prototype.push = function push(...values) {
    this.merge(values);
}

module.exports = Heap;