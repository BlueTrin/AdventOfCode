from aoc_lube import fetch

s = fetch(2018, 14)

recipes = bytearray([3, 7])
elf = (0, 1)

def next_recipes(recipes, elf):
    recipes.extend(int(c) for c in str(sum(recipes[i] for i in elf)))
    elf = [(i + recipes[i] + 1) % len(recipes) for i in elf]
    return recipes, elf

tgt = 880751
pattern = bytearray((int(c) for c in str(tgt)))
while len(recipes) < 10 + tgt or pattern not in recipes:
    print("try for 10000000")
    for i in range(10000000):
        recipes, elf = next_recipes(recipes, elf)

print("".join(str(r) for r in recipes[tgt:tgt+10]))
print(recipes.index(pattern))
