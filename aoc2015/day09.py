s = open("2015_09.txt").read()
towns = set()
dist = {}
for r in s.splitlines():
    if not r:
        continue

    d1, _, d2, _, t = r.split(" ")
    towns.update([d1, d2])
    dist[(d1, d2)] = int(t)
    dist[(d2, d1)] = int(t)

import itertools

min_path = sum(dist.values())
max_path = 0
for path in itertools.permutations(towns, len(towns)):
    pathl = 0
    for d1, d2 in zip(path, path[1:]):
        pathl += dist[(d1, d2)]
    print(f"{path}: {min_path}")
    min_path = min(min_path, pathl)
    max_path = max(max_path, pathl)

    
print(min_path)
print(max_path)