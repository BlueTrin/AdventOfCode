import networkx as nx
from aoc_lube import fetch
from utils2018.utils import Point
from itertools import permutations
from functools import cache

s = fetch(2016, 24)

G = nx.Graph()
FOURDIRS = [Point(0,1), Point(1,0), Point(0,-1), Point(-1,0)]

tgt = {}
for y, r in enumerate(s.splitlines()):
    for x, c in enumerate(r):
        if c == '#':
            continue
        if c != '.':
            tgt[int(c)] = Point(x, y)
        n = Point(x, y)
        G.add_node(n)
        for d in FOURDIRS:
            new_n = n + d
            if new_n in G:
                G.add_edge(n, new_n)

print(tgt)

@cache
def shortest_path_length(start, end):
    return nx.shortest_path_length(G, start, end)

min_len = 9999999999
for path in permutations([x for x in tgt.keys() if x != 0], len(tgt)-1):
    path = [0] + list(path)
    total = 0
    for i in range(len(path)-1):
        total += shortest_path_length(tgt[path[i]], tgt[path[i+1]])
#        total += nx.shortest_path_length(G, tgt[path[i]], tgt[path[i+1]])
        if total > min_len:
            break
    if min_len > total:
        min_len = total
        min_path = path

print("part1: ", min_path, min_len)

min_len = 9999999999
for path in permutations([x for x in tgt.keys() if x != 0], len(tgt)-1):
    if tuple(path) == (3, 2, 4, 5, 1, 7, 6):
        pass
    path = [0] + list(path) + [0]
    total = 0
    for i in range(len(path)-1):
        subtotal = shortest_path_length(tgt[path[i]], tgt[path[i+1]])
        total += subtotal
#        total += nx.shortest_path_length(G, tgt[path[i]], tgt[path[i+1]])
        if total > min_len:
            break
    if min_len > total:
        min_len = total
        min_path = path

print("part2: ", min_path, min_len)
# too high
# 0 -> 3 = 184
# 34
# 62
# 44
# 170
# 58
# 68
# 96