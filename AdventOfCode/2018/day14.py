from libs import *

# Parse input

score = read("example").splitlines()

nb_recipes = int(score[0])
score = [int(n) for n in list(score[-1])]

# Part 1


def scores(nb_recipes):
    recipes = [3, 7]
    e1, e2 = (0, 1)
    while len(recipes) < nb_recipes + 10:
        recipes.extend(int(n) for n in str(recipes[e1] + recipes[e2]))
        e1 = (e1 + recipes[e1] + 1) % len(recipes)
        e2 = (e2 + recipes[e2] + 1) % len(recipes)
    return recipes[nb_recipes : nb_recipes + 10]


part_one(scores(nb_recipes), sep="")

# Part 2


def find_score(score):
    recipes = [3, 7]
    e1, e2 = (0, 1)
    while recipes[-len(score) :] != score and recipes[-len(score) - 1 : -1] != score:
        recipes.extend(int(n) for n in str(recipes[e1] + recipes[e2]))
        e1 = (e1 + recipes[e1] + 1) % len(recipes)
        e2 = (e2 + recipes[e2] + 1) % len(recipes)
    if recipes[-len(score) - 1 : -1] == score:
        return len(recipes) - len(score) - 1
    else:
        return len(recipes) - len(score)


part_two(find_score(score))
