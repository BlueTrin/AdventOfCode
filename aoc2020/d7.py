from aoc_lube import fetch
import networkx as nx
from collections import deque

s = fetch(2020, 7)
G = nx.DiGraph()

for r in s.splitlines():
    left, right = r.split(' bags contain ')
    right_bags = right.split(', ')
    for bag in right_bags:
        bag = bag.replace('bags', '').replace('bag', '').replace('.', ''). strip()
        l, r = bag.split(' ', 1)
        if l == 'no':
            continue
        G.add_edge(left, r, weight=int(l))

print(f"Part1: {len(nx.ancestors(G, 'shiny gold'))}")

d = deque([('shiny gold', 1)])
bags = 0
while d:
    n, nq = d.popleft()
    for c in G.successors(n):
        m = G[n][c]['weight']
        d.append((c, m*nq))
        bags += m*nq

print(f"Part2: {bags}")



