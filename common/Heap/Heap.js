const Heap = require("collections/heap");

const _addEach = Heap.prototype.addEach;

Heap.prototype.merge = function merge(values) {
    let n = this.content.length;
    let k = values.length;

    this.content.push(...values);
    this.length += values.length;

    if (k * Math.log2(n + k) > n + k) {
        let m = Math.trunc(this.length / 2) - 1;
        for (let i = m; i >= 0; i--) {
            this.sink(i);
        }
    } else {
        for (let i = n; i < this.content.length; i++) {
            this.float(i);
        }
    }
};

Heap.prototype.addEach = function addEach(values, mapFn, thisp) {
    let newValues = [];
    this.add = function add(value) {
        newValues.push(value);
    };
    _addEach.call(this, values, mapFn, thisp);
    delete this.add;
    this.merge(newValues);
};

Heap.prototype.push = function push(...values) {
    this.merge(values);
};

Heap.prototype.reverse = function reverse() {
    // Inverse the order
    let oldContentCompare = this.contentCompare;
    this.contentCompare = function contentCompare(a, b) {
        return -oldContentCompare.call(this, a, b);
    };
    // Re-heapify the elements according to the new order
    let m = Math.trunc(this.length / 2) - 1;
    for (let i = m; i >= 0; i--) {
        this.sink(i);
    }
    // return current reference as result
    return this;
};

module.exports = Heap;
