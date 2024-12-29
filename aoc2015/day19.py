from aoc_lube import fetch
from collections import deque
from heapq import heappush, heappop

s = fetch(2015, 19)

trans_lst = []
trans_s_lst, mol = s.split('\n\n')
for trans_s in trans_s_lst.splitlines():
    src, dst = trans_s.split(' => ')
    trans_lst.append((src, dst))

mol = mol.strip()

seen = {}

for src, dst in trans_lst:
    for i in range(len(mol)):
        if mol[i:i+len(src)] == src:
            new_mol = mol[:i] + dst + mol[i+len(src):]
            seen[new_mol] = True

print(len(seen))

d = []
seen = {}
heappush(d, (len(mol), mol, 0, ()))
min_steps = 999999999999
min_sofar = None
while d:
    _, curr, steps, sofar = heappop(d)
    if curr in seen and seen[curr] <= steps:
        continue
    seen[curr] = steps

    if curr == 'e':
        if steps < min_steps:
            print(f"found min_steps={steps}")
            min_steps = steps
            min_sofar = sofar
        continue
    if steps > min_steps:
        continue

    for src, dst in trans_lst:
        for i in range(len(curr)):
            if curr[i:i + len(dst)] == dst:
                new_mol = curr[:i] + src + curr[i + len(dst):]
                if seen.get(new_mol, 0) > steps + 1:
                    continue

                heappush(d, (len(new_mol), new_mol, steps + 1, (src, dst) + sofar))

print(f"min_steps={min_steps}")
print(f"min_sofar={min_sofar}")