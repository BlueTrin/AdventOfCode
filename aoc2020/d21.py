from aoc_lube import fetch
from collections import defaultdict, Counter

s = fetch(2020, 21)

all_to_ing = defaultdict(set)
ing_count = Counter()
all_ings = set()
for r in s.splitlines():
    ing, allg = r.split(' (contains ')
    allg = allg.replace(')', '').split(', ')
    ing = ing.split(' ')
    all_ings |= set(ing)
    ing_count.update(ing)

    for a in allg:
        if not all_to_ing[a]:
            all_to_ing[a] = set(ing)
        else:
            all_to_ing[a] &= set(ing)

for a in all_to_ing.values():
    all_ings -= a

print(f"Part1: {sum(ing_count[i] for i in all_ings)}")
known = {}
while all_to_ing:
    known |= {al: next(iter(ingset)) for al, ingset in all_to_ing.items() if len(ingset) == 1}
    known_ings = set(known.values())
    all_to_ing = {al: ingset - known_ings for al, ingset in all_to_ing.items() if al not in known}

print(','.join([known[k] for k in sorted(known)]))