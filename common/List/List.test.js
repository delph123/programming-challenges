const { concat } = require("collections/shim-object");
const List = require("./DoublyLinkedList");
const Entry = List.Entry;
const listIterator = Entry.iterator;

describe("List", () => {
    it("Creates an empty list", () => {
        expect(new List().length).toEqual(0);
        expect(new List().head).toBeNull();

        expect(new List([]).length).toEqual(0);
        expect(new List(new Set()).head).toBeNull();
    });

    it("Creates a list from a list of values", () => {
        function* gen() {
            yield 1;
            yield 2;
        }
        function createList() {
            return new List(arguments);
        }
        expect(new List([1, 2, 3]).length).toEqual(3);
        expect(new List(new Set([1])).length).toEqual(1);
        expect(createList().length).toEqual(0);
        expect(createList("a", "b", "c", "d").length).toEqual(4);
        expect(new List(gen()).length).toEqual(2);
    });

    it("Converts the list to an array", () => {
        function* gen() {
            yield 1;
            yield 2;
        }
        function createList() {
            return new List(arguments);
        }
        expect(new List([1, 2, 3]).toArray()).toEqual([1, 2, 3]);
        expect(new List(new Set([1])).toArray()).toEqual([1]);
        expect(createList().toArray()).toEqual([]);
        expect(createList("a", "b", "c", "d").toArray().join("")).toEqual(
            "abcd"
        );
        expect(new List(gen()).toArray()).toEqual([1, 2]);
    });

    it("Adds elements at the end of the list", () => {
        const l = new List([1, 2]);
        expect(l.length).toEqual(2);
        l.push(3, 4);
        expect(l.length).toEqual(4);
        expect(l.toArray()).toEqual([1, 2, 3, 4]);
    });

    it("Clones the list", () => {
        const l = new List([1, 2, 3]);
        const h = l.clone();
        expect(l.toArray()).toEqual(h.toArray());
        h.push(4, 5, 6);
        expect(l.toArray()).toEqual([1, 2, 3]);
        expect(h.toArray()).toEqual([1, 2, 3, 4, 5, 6]);
    });

    it("Concatenates iterators", () => {
        const l = new List();
        g = l.concat("abc", new Set([1, 2, 3]), [true, false]);
        h = g.concat([{}, null]);

        expect(l.length).toBe(0);
        expect(g.toArray()).toEqual(["a", "b", "c", 1, 2, 3, true, false]);
        expect(h.toArray().length).toEqual(10);
    });

    it("Converts to string", () => {
        expect(new List("abcde").toString()).toEqual("a,b,c,d,e");
        expect(new List("abcde").join("")).toEqual("abcde");
    });

    it("Adds elements at the beginning", () => {
        const l = new List([1, 2]);
        expect(l.length).toEqual(2);
        l.unshift(3, 4);
        expect(l.length).toEqual(4);
        expect(l.toArray()).toEqual([3, 4, 1, 2]);
        expect(
            new List([5, 6]).mergeStart([1, 2], new Set([3, 4])).toArray()
        ).toEqual([1, 2, 3, 4, 5, 6]);
        expect(l.precat([5], [6, 7]).toArray()).toEqual([5, 6, 7, 3, 4, 1, 2]);
        expect(l.length).toEqual(4);
    });
});

describe("List reading", () => {
    let LIST;

    beforeEach(() => {
        LIST = new List([1, 2, 3, 4, 5, 6, 7]);
    });

    it("Find element at positive index", () => {
        for (let i = 0; i < LIST.length; i++) {
            expect(LIST.at(i)).toEqual(i + 1);
        }
        expect(LIST.at(7)).toBeUndefined();
        expect(LIST.at(17)).toBeUndefined();
    });

    it("Find element at negative index", () => {
        for (let i = 1; i <= LIST.length; i++) {
            expect(LIST.at(-i)).toEqual(LIST.length + 1 - i);
        }
        expect(LIST.at(-8)).toBeUndefined();
        expect(LIST.at(-17)).toBeUndefined();
    });

    it("Removes first element", () => {
        expect(LIST.shift()).toEqual(1);
        expect(LIST.length).toEqual(6);
        expect(LIST.head.value).toEqual(2);
        expect(LIST.head.prev).toBeNull();
        expect(LIST.head.next.value).toEqual(3);
        expect(LIST.tail.value).toEqual(7);
        expect(LIST.tail.next).toBeNull();
        expect(LIST.tail.prev.value).toEqual(6);
    });

    it("Removes first element with 2 elements", () => {
        LIST = new List([1, 2]);
        expect(LIST.shift()).toEqual(1);
        expect(LIST.length).toEqual(1);
        expect(LIST.head.value).toEqual(2);
        expect(LIST.head.prev).toBeNull();
        expect(LIST.head.next).toBeNull();
        expect(LIST.tail.value).toEqual(2);
        expect(LIST.tail.prev).toBeNull();
        expect(LIST.tail.next).toBeNull();
    });

    it("Removes first element with 1 element", () => {
        LIST = new List([1]);
        expect(LIST.shift()).toEqual(1);
        expect(LIST.length).toEqual(0);
        expect(LIST.head).toBeNull();
        expect(LIST.tail).toBeNull();
    });

    it("Removes first element with 0 element", () => {
        LIST = new List();
        expect(LIST.shift()).toBeUndefined();
        expect(LIST.length).toEqual(0);
        expect(LIST.head).toBeNull();
        expect(LIST.tail).toBeNull();
    });

    it("Removes last element", () => {
        expect(LIST.pop()).toEqual(7);
        expect(LIST.length).toEqual(6);
        expect(LIST.head.value).toEqual(1);
        expect(LIST.head.prev).toBeNull();
        expect(LIST.head.next.value).toEqual(2);
        expect(LIST.tail.value).toEqual(6);
        expect(LIST.tail.next).toBeNull();
        expect(LIST.tail.prev.value).toEqual(5);
    });

    it("Removes last element with 2 elements", () => {
        LIST = new List([1, 2]);
        expect(LIST.pop()).toEqual(2);
        expect(LIST.length).toEqual(1);
        expect(LIST.head.value).toEqual(1);
        expect(LIST.head.prev).toBeNull();
        expect(LIST.head.next).toBeNull();
        expect(LIST.tail.value).toEqual(1);
        expect(LIST.tail.prev).toBeNull();
        expect(LIST.tail.next).toBeNull();
    });

    it("Removes last element with 1 element", () => {
        LIST = new List([1]);
        expect(LIST.pop()).toEqual(1);
        expect(LIST.length).toEqual(0);
        expect(LIST.head).toBeNull();
        expect(LIST.tail).toBeNull();
    });

    it("Removes last element with 0 element", () => {
        LIST = new List();
        expect(LIST.shift()).toBeUndefined();
        expect(LIST.length).toEqual(0);
        expect(LIST.head).toBeNull();
        expect(LIST.tail).toBeNull();
    });

    it("Removes an element in the middle", () => {
        expect(LIST.remove(3)).toEqual(4);
        expect(LIST.length).toEqual(6);
        expect(LIST.at(2)).toEqual(3);
        expect(LIST._getEntry(2).next.value).toEqual(5);
        expect(LIST.at(3)).toEqual(5);
        expect(LIST._getEntry(3).prev.value).toEqual(3);
    });

    it("Removes middle element with 3 elements", () => {
        LIST = new List([1, 2, 3]);
        expect(LIST.remove(-2)).toEqual(2);
        expect(LIST.length).toEqual(2);
        expect(LIST.head.value).toEqual(1);
        expect(LIST.head.prev).toBeNull();
        expect(LIST.head.next).toBe(LIST.tail);
        expect(LIST.tail.value).toEqual(3);
        expect(LIST.tail.prev).toBe(LIST.head);
        expect(LIST.tail.next).toBeNull();
    });

    it("Removes element past the end", () => {
        LIST.remove(7);
        expect(LIST.toArray()).toEqual([1, 2, 3, 4, 5, 6, 7]);
        LIST.remove(-8);
        expect(LIST.toArray()).toEqual([1, 2, 3, 4, 5, 6, 7]);
    });

    it("Clears the content of the list", () => {
        LIST.clear();
        expect(LIST.length).toEqual(0);
        expect(LIST.head).toBeNull();
        expect(LIST.tail).toBeNull();
    });

    it("Reveses the list", () => {
        LIST.reverse();
        expect(LIST.toArray()).toEqual([7, 6, 5, 4, 3, 2, 1]);
        LIST.reverse();
        expect(LIST.toArray()).toEqual([1, 2, 3, 4, 5, 6, 7]);

        const g = LIST.reversed();
        expect(g.toArray()).toEqual([7, 6, 5, 4, 3, 2, 1]);
        expect(LIST.toArray()).toEqual([1, 2, 3, 4, 5, 6, 7]);
        const h = g.reversed();
        expect(h.toArray()).toEqual([1, 2, 3, 4, 5, 6, 7]);
        expect(g.toArray()).toEqual([7, 6, 5, 4, 3, 2, 1]);
        expect(LIST.toArray()).toEqual([1, 2, 3, 4, 5, 6, 7]);
    });
});

describe("List Entry", () => {
    it("Creates a list entry", () => {
        const e = new Entry(3);

        expect(e.value).toEqual(3);
        expect(e.next).toEqual(null);
        expect(e.prev).toEqual(null);
    });

    it("Adds a list entry before", () => {
        const e1 = new Entry(1);
        const e2 = new Entry(2);
        e2.addBefore(e1);

        expect(e1.prev).toBeNull();
        expect(e2.next).toBeNull();
        expect(e1.next).toBe(e2);
        expect(e2.prev).toBe(e1);
    });

    it("Adds a list entry after", () => {
        const e1 = new Entry(1);
        const e2 = new Entry(2);
        e1.addAfter(e2);

        expect(e1.prev).toBeNull();
        expect(e2.next).toBeNull();
        expect(e1.next).toBe(e2);
        expect(e2.prev).toBe(e1);
    });

    it("Creates a chain of entries from undefined", () => {
        const [start, end, size] = Entry.from();

        expect(start).toBeNull();
        expect(end).toBeNull();
        expect(size).toBe(0);
    });

    it("Creates a chain of entries from an empty list", () => {
        const [start, end, size] = Entry.from([]);

        expect(start).toBeNull();
        expect(end).toBeNull();
        expect(size).toBe(0);
    });

    it("Creates a chain of entries with single element", () => {
        const [start, end, size] = Entry.from(["e"]);

        expect(start.value).toEqual("e");
        expect(start).toBe(end);
        expect(size).toBe(1);
    });

    it("Creates a chain of entries with multiple elements", () => {
        const [start, end, size] = Entry.from(["a", "b", "c"]);

        expect(start.value).toEqual("a");
        expect(end.value).toEqual("c");
        expect(size).toBe(3);
        expect(start.next.next).toBe(end);
        expect(end.prev.prev.next.prev).toBe(start);
    });

    it("Collects multiple collections to create a chain", () => {
        const [start, end, size] = Entry.collect(["a"], [], ["b", "c"]);

        expect(start.value).toEqual("a");
        expect(end.value).toEqual("c");
        expect(size).toBe(3);
        expect(start.next.next).toBe(end);
        expect(end.prev.prev.next.prev).toBe(start);
    });
});

describe("List Iterator", () => {
    it("Creates a list iterator for an empty chain", () => {
        const iter = listIterator(null);
        expect(iter.next()).toEqual({ done: true });
        expect([...listIterator(null)]).toEqual([]);
    });

    it("Creates a list iterator for a chain with single element", () => {
        const iter = listIterator(new Entry("a"));
        expect(iter.next()).toEqual({ value: "a", done: false });
        expect(iter.next()).toEqual({ done: true });
        expect([...listIterator(new Entry("a"))]).toEqual(["a"]);
    });

    it("Creates a list iterator for a chain with multiple elements", () => {
        const head = Entry.collect("abc", ["d", "e"])[0];
        const iter = listIterator(head);

        expect(iter.next()).toEqual({ value: "a", done: false });
        expect(iter.next()).toEqual({ value: "b", done: false });
        expect(iter.next()).toEqual({ value: "c", done: false });
        expect(iter.next()).toEqual({ value: "d", done: false });
        expect(iter.next()).toEqual({ value: "e", done: false });
        expect(iter.next()).toEqual({ done: true });

        expect("".concat(...listIterator(head))).toEqual("abcde");
    });

    it("Creates a list iterator conforming to the Iterator protocol", () => {
        const head = Entry.collect("abc", ["d", "e"], new Set("fgh"))[0];
        const iter = listIterator(head);

        expect(iter.next()).toEqual({ value: "a", done: false });
        expect(iter.next("r")).toEqual({ value: "b", done: false });
        expect(iter.next(321)).toEqual({ value: "c", done: false });
        expect(iter.next()).toEqual({ value: "d", done: false });
        expect(iter.return("abc")).toEqual({ value: "abc", done: true });
        expect(iter.next()).toEqual({ done: true });

        const iter2 = listIterator(head);
        const err = new Error("hello");

        expect(iter2.next()).toEqual({ value: "a", done: false });
        expect(iter2.next("r")).toEqual({ value: "b", done: false });
        expect(iter2.throw.bind(iter2, err)).toThrow(err);
        expect(iter2.next()).toEqual({ done: true });

        const iter3 = listIterator(head);

        expect("".concat(...iter3)).toEqual("abcdefgh");
        expect(iter3.next()).toEqual({ done: true });
    });
});
