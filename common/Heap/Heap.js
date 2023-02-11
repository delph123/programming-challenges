const Heap = require("collections/heap");

const _addEach = Heap.prototype.addEach;

Heap.prototype.merge = function merge(values) {
    let n = this.content.length;
    let k = values.length;

    this.content.push(...values);
    this.length += values.length;

    if (k * Math.log2(n + k) > n + k) {
        // Use Floyd algorithm to build heap in O(n + k)
        let m = Math.trunc(this.length / 2) - 1;
        for (let i = m; i >= 0; i--) {
            this.sink(i);
        }
    } else {
        // Insert k elements one by one since float is O(log(n + k))
        for (let i = n; i < this.content.length; i++) {
            this.float(i);
        }
    }
};

Heap.prototype.addEach = function addEach(values, mapFn, thisp) {
    // Redifined add method to capture all added values
    let newValues = [];
    this.add = function add(value) {
        newValues.push(value);
    };
    // Call originial addEach method (inserting elements via add)
    _addEach.call(this, values, mapFn, thisp);
    // Restore original add method
    delete this.add;
    // Actually merge elements in bulk via merge method
    this.merge(newValues);
};

Heap.prototype.push = function push(...values) {
    // Redefined to support variadic & use bulk-merge for performance
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
