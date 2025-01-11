from aoc_lube import fetch
import networkx as nx

s = fetch(2019, 6)

G = nx.DiGraph()

for r in s.splitlines():
    a, b = r.split(')')
    G.add_edge(a, b)


total = 0
for n in G.nodes:
    total += len(nx.descendants(G,n))
print(total)

G = nx.Graph()

for r in s.splitlines():
    a, b = r.split(')')
    G.add_edge(a, b)

print(nx.shortest_path_length(G, 'YOU', 'SAN') - 2)
