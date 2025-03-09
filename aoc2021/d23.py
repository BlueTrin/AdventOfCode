from aoc_lube import fetch
import networkx as nx
from utils import Point
from collections import defaultdict

from heapq import heappop, heappush

s = fetch(2021, 23)

print(s)

G = nx.Graph()
pos_map = defaultdict(set)

for i_y, row in enumerate(s.splitlines()):
    for i_x, c in enumerate(row):
        if c != '#':
            pt = Point(i_x, i_y)
            G.add_node(pt)
            for n in pt.adjacent4():
                if n in G:
                    G.add_edge(pt, n)
            if c != '.':
                pos_map[c].add(pt)

pos = [p for l, cost in [('A', 1), ('B', 10), ('C', 100), ('D', 1000)] for p in pos_map[l]]
cost = [cost for l, cost in [('A', 1), ('B', 10), ('C', 100), ('D', 1000)] for p in pos_map[l]]

q = []
