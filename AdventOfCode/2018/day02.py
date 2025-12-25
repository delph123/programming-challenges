from libs import *

# Parse input

boxes = read("example")

if read.from_example:
    boxes, boxes_p2 = boxes.split("\n\n")
    boxes = boxes.splitlines()[1:]
    boxes_p2 = boxes_p2.splitlines()[1:]
else:
    boxes = boxes.splitlines()
    boxes_p2 = boxes

# Part 1


def replicate(box, times):
    return times in Counter(box).values()


part_one(sum(replicate(b, 2) for b in boxes) * sum(replicate(b, 3) for b in boxes))

# Part 2


def common(b0, b1):
    return "".join(x for x, y in zip(b0, b1) if x == y)


def most_similar(labels):
    return max(
        (common(b0, b1) for i, b0 in enumerate(labels) for b1 in labels[i + 1 :]),
        key=len,
    )


# The boxes with most similar labels are the ones which differs from a single character
part_two(most_similar(boxes_p2))
