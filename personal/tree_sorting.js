const ROOT_ID = -1;

class Tree {
    itemId;
    sortOrder;
    children;

    constructor(itemId, sortOrder, children) {
        this.itemId = itemId;
        this.sortOrder = sortOrder;
        this.children = children;
    }

    /**
     * An efficient algorithm which parses the items in one pass
     * and builds the tree by fragments.
     */
    static from(items) {
        const treeMap = new Map();
        // Initialize the root tree
        treeMap.set(ROOT_ID, new Tree(null, null, []));

        // Sort items globally by sort order
        const orderedItems = [...items].sort(
            ([, , sortOderA], [, , sortOderB]) => sortOderA - sortOderB
        );

        // Build the tree in one pass
        for (let [itemId, parentId, sortOrder] of orderedItems) {
            if (parentId == null) {
                parentId = ROOT_ID;
            }
            let node;
            if (treeMap.has(itemId)) {
                node = treeMap.get(itemId);
                node.itemId = itemId;
                node.sortOrder = sortOrder;
            } else {
                node = new Tree(itemId, sortOrder, []);
                treeMap.set(itemId, node);
            }
            if (treeMap.has(parentId)) {
                treeMap.get(parentId).children.push(node);
            } else {
                treeMap.set(parentId, new Tree(null, null, [node]));
            }
        }

        // console.log(
        //     [...treeMap.entries()]
        //         .sort(([a], [b]) => a - b)
        //         .map(([k, v]) => k + " => " + v.toString())
        //         .join("\n")
        // );

        return treeMap.get(ROOT_ID);
    }

    /**
     * A more simple but slower algorithm.
     */
    static from_quadratic(items, parent = null) {
        const root = new Tree(null, null, []);

        for (let [itemId, parentId, sortOrder] of items) {
            if (parentId == parent) {
                const subtree = Tree.from_quadratic(items, itemId);
                subtree.itemId = itemId;
                subtree.sortOrder = sortOrder;
                root.children.push(subtree);
            }
        }

        return root;
    }

    sort() {
        this.children.sort((a, b) => a.sortOrder - b.sortOrder);
        for (let child of this.children) {
            child.sort();
        }
        return this;
    }

    lines(parent = null, from = 0) {
        let l = [[this.itemId, parent, this.sortOrder, from]];
        let num = from + 1;
        for (let child of this.children) {
            const childLines = child.lines(this.itemId, num);
            l = l.concat(childLines);
            num += childLines.length;
        }
        return l;
    }

    toString() {
        return `${this.itemId} / ${this.sortOrder} / [${this.children
            .map((c) => c.itemId)
            .join(", ")}]`;
    }
}

module.exports = Tree;
