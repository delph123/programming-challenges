class AbstractCollection {
    push(...values) {
        return this.merge(values);
    }

    concat(...collections) {
        return this.clone().merge(...collections);
    }

    reversed() {
        return this.clone().reverse();
    }

    toString() {
        return this.join();
    }
}

module.exports = AbstractCollection;
