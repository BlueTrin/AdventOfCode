from aoc_lube import fetch
from collections import deque

s = fetch(2019, 14)

# print(s)

rec = {}

for r in s.splitlines():
    ingre_s, result_s = r.split(' => ')
    ingre = [(int((tkn:=ingre_it.split())[0]), tkn[1]) for ingre_it in ingre_s.split(', ')]
    res = (int((tkn:=result_s.split())[0]), tkn[1])

    rec[res[1]] = (res[0], ingre)

def solve_fuel(fuel_qty):
    q = deque([(fuel_qty, "FUEL")])
    ore_count = 0
    stock = {}
    while q:
        qty, ing = q.popleft()
        if ing == "ORE":
            ore_count += qty
            continue
        rec_qty, sub_ing = rec[ing]
        mult = (qty + rec_qty - 1 - stock.get(ing, 0)) // rec_qty
        stock[ing] = stock.get(ing, 0) + rec_qty * mult - qty

        for sub_qty, sub in sub_ing:
            q.append((sub_qty * mult, sub))
    return ore_count
print(f"part 1: {solve_fuel(1)}")

# 483766 good
tgt = 1000000000000
guess = int(tgt / solve_fuel(1)) # ore_count


val = solve_fuel(guess)
if val < tgt:
    low = guess
    high = int(low * ((tgt - val) / val + 1) * 1.2)
else:
    high = guess
    low = int(tgt/guess * 0.5)

while high - low > 1:
    guess = (high + low) // 2
    val = solve_fuel(guess)
    if val < tgt:
        low = guess
    else:
        high = guess
print(f"part 2: {int(low)}")

