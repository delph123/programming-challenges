function defaultCompare(a, b) {
    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
}

function noop() {}

function expand(collection) {
    if (collection == null) {
        return [];
    } else if (Array.isArray(collection)) {
        return collection;
    } else if (typeof collection[Symbol.iterator] === "function") {
        return [...collection];
    } else if (typeof collection.length === "number") {
        return new Array(collection.length)
            .fill(0)
            .map((_, i) => collection[i]);
    }
}

function collect(collections) {
    if (!collections || collections.length === 0) {
        return [];
    }

    return [].concat(...collections.map(expand));
}

class BinaryMaxHeap {
    content;
    length;
    /** The comparison function */
    compare;
    changeListner;

    constructor(initialValues, compare, changeListner) {
        this.content = [];
        this.length = 0;
        this.compare = compare || defaultCompare;
        this.changeListner = changeListner || noop;
        this.merge(initialValues);
    }

    push(...values) {
        return this.merge(values);
    }

    pop() {
        return this.remove(0);
    }

    concat(...collections) {
        return this.clone().merge(...collections);
    }

    remove(index) {
        if (index >= this.length) {
            return undefined;
        }

        let value = this.content[index];
        let last = this.content.pop();
        this.length--;

        if (index === this.length) {
            this.changeListner(last, undefined, this);
            return last;
        }

        this.content[index] = last;
        this.changeListner(value, undefined, this);
        this.changeListner(last, index, this);

        let compareLast = this.compare(last, value);
        if (compareLast > 0) {
            this.heapifyUp(index);
        } else if (compareLast < 0) {
            this.heapifyDown(index);
        }

        return value;
    }

    merge(...collections) {
        let values = collect(collections);

        if (!values || values.length <= 0) {
            return;
        }

        let n = this.content.length;
        let k = values.length;

        this.content = this.content.concat(values);
        this.length += values.length;

        values.forEach((val, idx) => {
            this.changeListner(val, n + idx, this);
        });

        if (k * Math.log2(n + k) > n + k) {
            let m = Math.trunc(this.length / 2) - 1;
            for (let i = m; i >= 0; i--) {
                this.heapifyDown(i);
            }
        } else {
            for (let i = n; i < this.content.length; i++) {
                this.heapifyUp(i);
            }
        }

        return this;
    }

    heapifyUp(index) {
        let i = index;
        let j = Math.trunc((i - 1) / 2);
        while (i > 0 && this.compare(this.content[i], this.content[j]) > 0) {
            this.swap(i, j);
            i = j;
            j = Math.trunc((i - 1) / 2);
        }
        return this;
    }

    heapifyDown(index) {
        let i = index;
        let j = 2 * i + 1;
        if (
            j + 1 < this.length &&
            this.compare(this.content[j + 1], this.content[j]) > 0
        ) {
            j++;
        }
        while (
            j < this.length &&
            this.compare(this.content[i], this.content[j]) < 0
        ) {
            this.swap(i, j);
            i = j;
            j = 2 * i + 1;
            if (
                j + 1 < this.length &&
                this.compare(this.content[j + 1], this.content[j]) > 0
            ) {
                j++;
            }
        }
        return this;
    }

    clear() {
        let values = this.content;
        this.content = [];
        this.length = 0;

        values.forEach((val) => this.changeListner(val, undefined, this));
    }

    toArray() {
        return this.content.slice();
    }

    [Symbol.iterator]() {
        return this.content[Symbol.iterator]();
    }

    reverse() {
        // Inverse the order
        let oldCompare = this.compare;
        this.compare = function compare(a, b) {
            return -oldCompare.call(this, a, b);
        };
        // Re-heapify the elements according to the new order
        let m = Math.trunc(this.length / 2) - 1;
        for (let i = m; i >= 0; i--) {
            this.heapifyDown(i);
        }
        // return current reference as result
        return this;
    }

    clone() {
        return new BinaryMaxHeap(
            this.content,
            this.compare,
            this.changeListner
        );
    }

    reversed() {
        return this.clone().reverse();
    }

    swap(i, j) {
        if (i !== j) {
            let t = this.content[i];
            this.content[i] = this.content[j];
            this.content[j] = t;
            this.changeListner(this.content[i], i, this);
            this.changeListner(this.content[j], j, this);
        }
        return this;
    }

    map(fn, thisp) {
        return this.content.map(fn, thisp);
    }

    forEach(fn, thisp) {
        return this.content.forEach(fn, thisp);
    }

    reduce(fn, thisp) {
        return this.content.reduce(fn, thisp);
    }

    reduceRight(fn, thisp) {
        return this.content.reduceRight(fn, thisp);
    }

    join(sep) {
        return this.content.join(sep);
    }

    toString() {
        return this.join();
    }
}

BinaryMaxHeap.prototype.addEach = BinaryMaxHeap.prototype.merge;
BinaryMaxHeap.prototype.add = BinaryMaxHeap.prototype.push;

module.exports = BinaryMaxHeap;
