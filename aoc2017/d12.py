from aoc_lube import fetch
import networkx as nx

s = fetch(2017, 12)

G = nx.Graph()

for r in s.splitlines():
    src, dst_csv = r.split(' <-> ')
    dsts = dst_csv.split(', ')
    for d in dsts:
        G.add_edge(src, d)

print(f"Part1: {len(nx.node_connected_component(G, '0'))}")
print(f"Part2: {nx.number_connected_components(G)}")
