/**
 * Implements a simple Least Recently Used Cache.
 *
 * A least recently used cache is a capacity-bound cache which evicts the element that
 * was least recently used (accessed or mutated) whenever the capacity limit is hit.
 *
 * This implementation uses a vanilla-JS Map which maintains the original insertion order
 * of the keys in addition to the mapping itself. This invariant is used to evict elements
 * when necessary. The implementation also maintains compatibility with the Map interface
 * for most part (i.e. for methods which makes as part of the interface of a Cache).
 *
 * The client may provide a function to compute an element's value when the value couldn't
 * be found in the cache (a cache miss). This allows transparent usage of the cache (values
 * are retrieved from the cache in case of cache hit and derived from the function when
 * it could not be found in the cache).
 */
class LRUCache {
    /** The real cache */
    cache;
    /** The maximum capacity of the cache */
    capacity;
    /** A function to derive the value from the key, used during cache miss */
    _onCacheMissed;

    constructor(capacity = 10000, { onCacheMissed } = {}) {
        this.cache = new Map();
        this.capacity = capacity;
        this._onCacheMissed = onCacheMissed;
    }

    /**
     * Check if the element exists in the cache.
     *
     * Note: If a cache miss handler was provided, it won't be called by this
     * method in case that there is no value in the cache.
     *
     * @returns whether an element with the specified key exists or not
     */
    has(key) {
        return this.cache.has(key);
    }

    /**
     * Returns the specified element from the cache if it was found. If the key is not
     * found, will try to deviate the value from the cache miss handler if possible.
     *
     * @returns the element associated with the specified key or undefined
     */
    get(key) {
        // If we don't find the key in the cache, regenerate it
        // from the _onCacheMissed handler if it was provided
        if (!this.cache.has(key)) {
            if (this._onCacheMissed) {
                const v = this._onCacheMissed(key);
                if (v !== undefined) {
                    this.set(key, v);
                    return v;
                }
            }
            return undefined;
        }

        const val = this.cache.get(key);

        // Remove & set the key again in the cache to update the
        // order of this key and put it at the end (since it is
        // the most recently used key now)
        this.cache.delete(key);
        this.cache.set(key, val);

        return val;
    }

    /**
     * Adds a new element with a specified key and value to the cache.
     *
     * If an element with the same key already exists, the element will
     * be overwritten.
     */
    set(key, val) {
        // Same thing as for get, we delete the key before to
        // set it again, in order to maintain the key order
        this.cache.delete(key);

        if (this.cache.size >= this.capacity) {
            // We've reached the capacity limitation, we'll need
            // to remove the least recently used key. Since the
            // underlying Map maintain the key in insertion order
            // the least recently used key is the first key from
            // the cache
            this.cache.delete(this.cache.keys().next().value);
        }

        this.cache.set(key, val);

        return this;
    }

    /**
     * Delete / evict an element from the cache.
     *
     * @returns true if this element was in the cache and has been removed or false
     */
    delete(key) {
        return this.cache.delete(key);
    }

    /**
     * Clear the cache content.
     */
    clear() {
        this.cache.clear();
    }
}

module.exports = LRUCache;
