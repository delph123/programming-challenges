from libs import *

# Parse input

license_numbers = [int(n) for n in read("example").split()]

# Part 1


def tree():
    def subtree(index):
        children = license_numbers[index]
        mentries = license_numbers[index + 1]
        nodes = []
        index += 2
        for _ in range(children):
            node, index = subtree(index)
            nodes.append(node)
        metadata = license_numbers[index : index + mentries]
        return ((nodes, metadata), index + mentries)

    return subtree(0)[0]


def traverse(t):
    children, metadata = t
    yield from metadata
    for child in children:
        yield from traverse(child)


part_one(sum(traverse(tree())))

# Part 2


def value(t):
    children, metadata = t
    if len(children) == 0:
        return sum(metadata)
    indexes = Counter(metadata)
    return sum(
        value(children[c - 1]) * n for c, n in indexes.items() if 0 < c <= len(children)
    )


part_two(value(tree()))
