from aoc_lube import fetch
import networkx as nx
from collections import Counter, deque

s = fetch(2021, 12)

# s = '''start-A
# start-b
# A-c
# A-b
# b-d
# A-end
# b-end'''
print(s)
G = nx.Graph()

small_caves = set()
for r in s.splitlines():
    d1, d2 = r.split('-')
    G.add_edge(d1, d2)
    for d in (d1, d2):
        # if d in ('start', 'end'):
        #     continue
        if 'a' <= d[0] <= 'z':
            small_caves.add(d)

d = deque([('start', set(['start']))])
p1 = 0
while d:
    curr, seen = d.pop()
    for n in G.neighbors(curr):
        if n in small_caves and n in seen:
            continue
        if n == 'end':
            print(seen)
            p1 += 1
            continue
        d.append((n, seen | {n}))

print(f"Part1: {p1}")


d = deque([('start', ('start', ))])
p2 = 0
while d:
    curr, seen = d.pop()
    for n in G.neighbors(curr):
        if n == 'start':
            continue
        if n == 'end':
            # print(seen)
            p2 += 1
            continue
        next_seen = seen + (n, )

        c = Counter(x for x in next_seen if x in small_caves)
        if max(c.values()) > 2:
            continue
        if len(tuple(k for k,v in c.items() if v > 1)) > 1:
            continue

        d.append((n, next_seen))

print(f"Part2: {p2}")