const { collect } = require("../Collection/util");
const AbstractCollection = require("../Collection/AbstractCollection");

class DoublyLinkedList {
    length;

    head;
    tail;

    constructor(initialValues) {
        this.head = null;
        this.tail = null;
        this.length = 0;
        this.mergeEnd(initialValues);
    }

    mergeEnd(...collections) {
        const [start, end, size] = ListEntry.collect(...collections);

        if (size === 0) {
            return this;
        }

        if (this.length === 0) {
            this.head = start;
        } else {
            this.tail.addAfter(start);
        }
        this.tail = end;

        this.length += size;

        return this;
    }

    mergeStart(...collections) {
        const [start, end, size] = ListEntry.collect(...collections);

        if (size === 0) {
            return this;
        }

        if (this.length === 0) {
            this.tail = end;
        } else {
            this.head.addBefore(end);
        }
        this.head = start;

        this.length += size;

        return this;
    }

    _getEntry(index) {
        if (index >= 0) {
            let current = this.head;
            let i = index;
            while (i > 0 && current != null) {
                current = current.next;
                i--;
            }
            return current;
        } else {
            let current = this.tail;
            let i = -index - 1;
            while (i > 0 && current != null) {
                current = current.prev;
                i--;
            }
            return current;
        }
    }

    at(index) {
        return this._getEntry(index)?.value;
    }

    unshift(...values) {
        return this.mergeStart(values);
    }

    precat(...collections) {
        return this.clone().mergeStart(...collections);
    }

    pop() {
        return this.remove(-1);
    }

    shift() {
        return this.remove(0);
    }

    remove(index) {
        let e = this._getEntry(index);

        if (e == null) {
            return;
        }

        this.length--;

        if (this.length === 0) {
            this.head = null;
            this.tail = null;

            return e.value;
        }

        if (e === this.head) {
            this.head = e.next;
            this.head.prev = null;
        } else if (e === this.tail) {
            this.tail = e.prev;
            this.tail.next = null;
        } else {
            e.prev.next = e.next;
            e.next.prev = e.prev;
        }

        e.prev = null;
        e.next = null;

        return e.value;
    }

    [Symbol.iterator]() {
        return ListEntry.iterator(this.head);
    }

    toArray() {
        return [...this];
    }

    join(sep) {
        return this.toArray().join(sep);
    }

    clone() {
        return new DoublyLinkedList(this);
    }

    clear() {
        this.length = 0;
        this.head = null;
        this.tail = null;
    }

    reverse() {
        let values = this.toArray().reverse();
        this.clear();
        return this.merge(values);
    }
}

DoublyLinkedList.prototype.merge = DoublyLinkedList.prototype.mergeEnd;
DoublyLinkedList.prototype.push = AbstractCollection.prototype.push;
DoublyLinkedList.prototype.concat = AbstractCollection.prototype.concat;
DoublyLinkedList.prototype.reversed = AbstractCollection.prototype.reversed;
DoublyLinkedList.prototype.toString = AbstractCollection.prototype.toString;

class ListEntry {
    constructor(value, prev = null, next = null) {
        this.value = value;
        this.prev = prev;
        this.next = next;
    }

    addAfter(node) {
        this.next = node;
        node.prev = this;
    }

    addBefore(node) {
        this.prev = node;
        node.next = this;
    }

    static from(values) {
        if (!values || values.length === 0) {
            return [null, null, 0];
        }

        const start = new ListEntry(values[0]);
        let end = start;

        for (let i = 1; i < values.length; i++) {
            end.addAfter(new ListEntry(values[i]));
            end = end.next;
        }

        return [start, end, values.length];
    }

    static collect(...collections) {
        return ListEntry.from(collect(collections));
    }

    static *iterator(head) {
        let current = head;
        while (current != null) {
            yield current.value;
            current = current.next;
        }
    }
}

DoublyLinkedList.Entry = ListEntry;

module.exports = DoublyLinkedList;
