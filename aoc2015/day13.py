import itertools


tbl = {}

for r in open("2015_13.txt").read().splitlines():
    if not r:
        continue
    w = r.replace(".", "").split(" ")

    c1 = w[0]
    c2 = w[-1]
    g = int(w[3]) * (-1 if w[2] == 'lose' else 1)
    tbl[(c1, c2)] = g

guests = sorted(set(itertools.chain(*tbl.keys())))
print(guests)
max_fun = -100000000
for c in itertools.permutations(guests, len(guests)):
    fun = 0
    for i in range(len(c)):
        fun += tbl[(c[i], c[(i+1) % len(c)])]
        fun += tbl[(c[i], c[i-1])]
    max_fun = max(max_fun, fun)

print(max_fun)

guests.append("weirdo")
for g in guests:
    tbl[(g, "weirdo")] = 0
    tbl[("weirdo", g)] = 0

max_fun = -100000000
for c in itertools.permutations(guests, len(guests)):
    fun = 0
    for i in range(len(c)):
        fun += tbl[(c[i], c[(i+1) % len(c)])]
        fun += tbl[(c[i], c[i-1])]
    max_fun = max(max_fun, fun)

print(max_fun)
