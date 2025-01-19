from aoc_lube import fetch
import networkx as nx
from d10 import knot_hash2

s = fetch(2017, 14)
print(s)

def disk(s):
    G = nx.Graph()

    used = 0
    for i in range(128):
        knot = knot_hash2(f"{s}-{i}")
        r = f"{knot:0128b}"
        used += r.count('1')
        for x, c in enumerate(r):
            if c == '1':
                G.add_node((i, x))
                if (i-1, x) in G:
                    G.add_edge((i, x), (i-1, x))
                if (i, x-1) in G:
                    G.add_edge((i, x), (i, x-1))
    return used, nx.number_connected_components(G)

d, r = disk("flqrgnkx")
assert d == 8108
assert r == 1242

d, r = disk(s)
print(f"Part1: {d}")
print(f"Part2: {r}")
