from libs import *

# Parse input

matcher = create_matcher(
    [
        ("swap position {int} with position {int}", ("swap_pos", 0, 1)),
        ("swap letter {str} with letter {str}", ("swap", 0, 1)),
        ("rotate {str} {int} step(?:s?)", ("rotate", 0, 1)),
        ("rotate based on position of letter {str}", ("rotate", "letter", 0)),
        ("move position {int} to position {int}", ("move", 0, 1)),
        ("reverse positions {int} through {int}", ("reverse", 0, 1)),
    ]
)

rules = [matcher(r) for r in read_lines("example")]

password = "abcde" if read.from_example else "abcdefgh"
scrambled_password = "decab" if read.from_example else "fbgdceah"

# Part 1


def scramble(rules, text):
    text = list(text)
    for rule, x, y in rules:
        match rule:
            case "swap_pos":
                text[x], text[y] = text[y], text[x]
            case "swap":
                i = text.index(x)
                j = text.index(y)
                text[i], text[j] = text[j], text[i]
            case "rotate":
                if x == "letter":
                    x = "right"
                    y = 1 + text.index(y)
                    if y > 4:
                        y += 1
                    y %= len(text)
                if x == "right":
                    text = text[-y:] + text[:-y]
                else:
                    text = text[y:] + text[:y]
            case "move":
                c = text.pop(x)
                text.insert(y, c)
            case "reverse":
                text[x : y + 1] = list(reversed(text[x : y + 1]))
    return text


part_one(scramble(rules, password), sep="")

# Part 2


def unscramble(rules, text):
    text = list(text)
    for rule, x, y in reversed(rules):
        match rule:
            case "swap_pos":
                text[x], text[y] = text[y], text[x]
            case "swap":
                i = text.index(x)
                j = text.index(y)
                text[i], text[j] = text[j], text[i]
            case "rotate":
                if x == "letter":
                    x = "right"
                    i = text.index(y)
                    for j in range(len(text)):
                        z = 2 * j + 1
                        if j >= 4:
                            z += 1
                        z %= len(text)
                        if z == i:
                            y = (j + (1 if j < 4 else 2)) % len(text)
                            break
                if x == "left":
                    text = text[-y:] + text[:-y]
                else:
                    text = text[y:] + text[:y]
            case "move":
                c = text.pop(y)
                text.insert(x, c)
            case "reverse":
                text[x : y + 1] = list(reversed(text[x : y + 1]))
    return text


part_two(unscramble(rules, scrambled_password), sep="")
