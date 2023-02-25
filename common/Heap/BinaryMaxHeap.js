
function defaultCompare(a, b) {
    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
}

function noop() {}

class BinaryMaxHeap {
    content;
    length;
    /** The comparison function */
    compare;
	observer;

    constructor(initialValues, compare, observer) {
        this.content = [];
        this.length = 0;
        this.compare = compare || defaultCompare;
        this.observer = observer || noop;
        this.merge(initialValues);
    }

	push(...values) {
		this.merge(values);
	}

	pop() {
		return this.remove(0);
	}
	
	concat(...values) {
		return new BinaryMaxHeap(this.content.concat(...values), this.compare, this.observer);
	}

	remove(index) {
		let value = this.content[index];
		let last = this.content.pop();
		this.length--;

		if (index === this.length) {
			this.observer(last, undefined, this);
			return last;
		}

		this.content[index] = last;
		this.observer(value, undefined, this);
		this.observer(last, index, this);

		let compareLast = this.compare(last, value);
		if (compareLast > 0) {
			this.heapifyUp(index);
		} else if (compareLast < 0) {
			this.heapifyDown(index);
		}

		return value;
	}
		
	merge(values) {
        let n = this.content.length;
        let k = values.length;
    
        this.content = this.content.concat(values);
        this.length += values.length;

		this.content.forEach((val, idx) => {
			this.observer(val, idx, this);
		})
    
        if (k * Math.log2(n+k) > n + k) {
            let m = Math.trunc(this.length / 2) - 1;
            for (let i = m; i >= 0; i--) {
                this.heapifyDown(i);
            }
        } else {
            for (let i = n; i < this.content.length; i++) {
                this.heapifyUp(i);
            }
        }
	}
	
	heapifyUp(index) {
		let i = index;
		let j = Math.trunc((i-1)/2);
		while (i > 0 && this.compare(this.content[i], this.content[j]) > 0) {
			this.swap(i, j);
			i = j;
			j = Math.trunc((i-1)/2);
		}
	}
	
	heapifyDown(index) {
		let i = index;
		let j = 2 * i + 1;
		if (j+1 < this.length && this.compare(this.content[j+1], this.content[j]) > 0) {
			j++;
		}
		while (j < this.length && this.compare(this.content[i], this.content[j]) < 0) {
			this.swap(i, j);
			i = j;
			j = 2 * i + 1;
			if (j+1 < this.length && this.compare(this.content[j+1], this.content[j]) > 0) {
				j++;
			}
		}
	}
	
	swap(i, j) {
		if (i !== j) {
			let t = this.content[i];
			this.content[i] = this.content[j];
			this.content[j] = t;
			this.observer(this.content[i], i, this);
			this.observer(this.content[j], j, this);
		}
	}
	
	check() {
		for (let i = 1; i < this.length; i++) {
			let j = Math.trunc((i-1)/2);
			if (this.compare(this.content[i], this.content[j]) > 0) {
				console.log("> Big problem :", i, j);
			}
		}
	}

	map(fn) {
		return this.content.map(fn);
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