const LRUCache = require("./LRUCache");

const CACHE_CAPACITY = 5;
let LRU_CACHE;

beforeEach(() => {
  // Recreate new LRU Cache
  LRU_CACHE = new LRUCache(CACHE_CAPACITY);
  LRU_CACHE.set("a", 1).set("b", 2).set("c", 3);
});

afterAll(() => {
  LRU_CACHE = undefined;
});

test("It accepts an empty constructor", () => {
  expect(new LRUCache()).toBeInstanceOf(LRUCache);
});

test("It caches records provided", () => {
  expect(LRU_CACHE.has("a")).toBe(true);
  expect(LRU_CACHE.get("b")).toBe(2);
});

test("It returns undefined for unknown keys", () => {
  expect(LRU_CACHE.has("x")).toBe(false);
  expect(LRU_CACHE.get("y")).toBeUndefined();
});

test("It deletes keys", () => {
  expect(LRU_CACHE.get("a")).toBe(1);
  LRU_CACHE.delete("a");
  expect(LRU_CACHE.get("a")).toBeUndefined();
  expect(LRU_CACHE.get("b")).toBe(2);
  LRU_CACHE.clear();
  expect(LRU_CACHE.get("b")).toBeUndefined();
});

test("It removes oldest keys to keep capacity", () => {
  for (let i = 0; i < CACHE_CAPACITY; i++) {
    LRU_CACHE.set("k" + i, i);
  }

  expect(LRU_CACHE.has("a")).toBe(false);
  expect(LRU_CACHE.get("c")).toBeUndefined();

  for (let i = 0; i < CACHE_CAPACITY; i++) {
    expect(LRU_CACHE.get("k" + i)).toBe(i);
  }
});

test("It updates key order at read", () => {
  // Reach capacity
  LRU_CACHE.set("d", 4).set("e", 5);
  // Read cache for "a" & "c"
  expect(LRU_CACHE.get("a")).toBe(1);
  expect(LRU_CACHE.get("c")).toBe(3);
  // Overflow => LRU cache ("b" & "d") will be removed
  LRU_CACHE.set("f", 6).set("g", 7);
  // "b" and "d" are indeed gone
  expect(LRU_CACHE.has("b")).toBe(false);
  expect(LRU_CACHE.get("d")).toBeUndefined();
  expect(LRU_CACHE.get("e")).toBe(5);
});

test("It updates key order at write/replace", () => {
  // Reach capacity
  LRU_CACHE.set("d", 4).set("e", 5);
  // Update cache for "a" & "c"
  LRU_CACHE.set("a", 6).set("c", 7);
  // Overflow => LRU cache ("b" & "d") will be removed
  LRU_CACHE.set("f", 8).set("g", 9);
  // "b" and "d" are indeed gone
  expect(LRU_CACHE.has("b")).toBe(false);
  expect(LRU_CACHE.get("d")).toBeUndefined();
  expect(LRU_CACHE.get("e")).toBe(5);
});

test("It accepts a cache miss handler", () => {
  // Create a cache with a cache miss handler generating keys
  // like: a -> 1, b -> 2, c -> 3, etc.
  const cache = new LRUCache(CACHE_CAPACITY, {
    onCacheMissed: (c) => c.charCodeAt(0) - "a".charCodeAt(0) + 1,
  });
  // Fill a few keys matching the pattern
  cache.set("a", 1).set("b", 2).set("c", 3);
  // Read the cache for twice it's size (keys will be generated on the fly)
  for (let i = 0; i < 2 * CACHE_CAPACITY; i++) {
    expect(cache.get(String.fromCharCode(i + "a".charCodeAt(0)))).toBe(i + 1);
  }
  // Oldest keys are gone
  for (let i = 0; i < CACHE_CAPACITY; i++) {
    expect(cache.has(String.fromCharCode(i + "a".charCodeAt(0)))).toBe(false);
  }
  // Newest keys are still there
  for (let i = CACHE_CAPACITY; i < 2 * CACHE_CAPACITY; i++) {
    expect(cache.has(String.fromCharCode(i + "a".charCodeAt(0)))).toBe(true);
  }
});

test("It doesn't store the handler's result when undefined", () => {
  // Create a cache with a cache miss handler generating keys
  // for pair numbers only
  const cache = new LRUCache(CACHE_CAPACITY, {
    onCacheMissed: (c) => (c % 2 === 0 ? c : undefined),
  });
  // Fill a few keys matching the pattern
  cache.set(1, 1).set(2, 2);
  // Check keys from cache
  expect(cache.get(1)).toBe(1);
  expect(cache.get(2)).toBe(2);
  // Check pair key for cache miss handler
  expect(cache.get(4)).toBe(4);
  expect(cache.has(4)).toBe(true);
  // Check impair key for cache miss handler
  expect(cache.get(5)).toBeUndefined();
  expect(cache.has(5)).toBe(false);
});
