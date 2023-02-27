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

module.exports = {
    defaultCompare,
    noop,
    collect,
    expand,
};
