import re
from itertools import permutations
import math

inp = '''Sprinkles: capacity 5, durability -1, flavor 0, texture 0, calories 5
PeanutButter: capacity -1, durability 3, flavor 0, texture 0, calories 1
Frosting: capacity 0, durability -1, flavor 4, texture 0, calories 6
Sugar: capacity -1, durability 0, flavor 0, texture 2, calories 8'''

ingredients = {}
for line in inp.splitlines():
    name, properties = line.split(': ')
    props = list(map(int, re.findall(r'-?\d+', properties)))
    ingredients[name] = props

best_score = 0
best_score500 = 0

all_combis = [(x1, x2, x3, x4) for x1 in range(101) for x2 in range(101-x1) for x3 in range(101-x1-x2) for x4 in range(101-x1-x2-x3) if x1+x2+x3+x4 == 100]
for amounts in all_combis:
        recipe_vals = [max(sum(x), 0) for x in zip(*[[att * amount for att in att_vals]
                               for (att_vals, amount) in zip(
                ingredients.values(), amounts)])]
        best_score = max(best_score, math.prod(recipe_vals[:-1]))
        if recipe_vals[-1] == 500:
            best_score500 = max(best_score500, math.prod(recipe_vals[:-1]))

print(best_score)
print(best_score500)
