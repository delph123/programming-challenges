function defaultCompare(a, b) {
    if (a < b) return -1;
    if (a > b) return 1;
    return 0;
}

function sum(...values) {
    return values.reduce((s, c) => s + c);
}

function product(...values) {
    return values.reduce((s, c) => s * c);
}

function* zip(...iterables) {
    if (iterables.length === 0) {
        return;
    }

    const iterators = iterables.map((iter) => iter[Symbol.iterator]());
    let iteratorResults = iterators.map((it) => it.next());

    while (!iteratorResults.some((res) => res.done)) {
        yield iteratorResults.map((res) => res.value);
        iteratorResults = iterators.map((it) => it.next());
    }
}

function* zipLongest(...iterablesAndfillValue) {
    if (iterablesAndfillValue.length === 0) {
        return;
    }

    let iterables = iterablesAndfillValue;
    let fillValue = undefined;

    if (
        typeof iterablesAndfillValue[iterablesAndfillValue.length - 1][
            Symbol.iterator
        ] !== "function"
    ) {
        iterables = [...iterablesAndfillValue];
        fillValue = iterables.pop();

        if (iterables.length === 0) {
            return;
        }
    }

    const iterators = iterables.map((iter) => iter[Symbol.iterator]());
    let iteratorResults = iterators.map((it) => it.next());

    while (iteratorResults.some((res) => !res.done)) {
        yield iteratorResults.map((res) => (res.done ? fillValue : res.value));
        iteratorResults = iterators.map((it) => it.next());
    }
}

function noop() {}

function expand(collection) {
    if (collection == null) {
        return [];
    } else if (Array.isArray(collection)) {
        return collection;
    } else {
        return Array.from(collection);
    }
}

function collect(collections) {
    if (!collections || collections.length === 0) {
        return [];
    }

    return [].concat(...collections.map(expand));
}

function* range(from, to = undefined, step = 1) {
    let start = from;
    let end = to;
    if (to == null) {
        start = 0;
        end = from;
    }

    if (step > 0) {
        for (let v = start; v < end; v += step) {
            yield v;
        }
    } else {
        for (let v = start; v > end; v += step) {
            yield v;
        }
    }
}

module.exports = {
    defaultCompare,
    noop,
    collect,
    expand,
    zip,
    zipLongest,
    sum,
    product,
    range,
};
