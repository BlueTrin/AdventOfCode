from aoc_lube import fetch
import networkx as nx
from utils import Point

s = fetch(2021, 15)

# s = '''1163751742
# 1381373672
# 2136511328
# 3694931569
# 7463417111
# 1319128137
# 1359912421
# 3125421639
# 1293138521
# 2311944581'''
#print(s)

G = nx.DiGraph()

for iy, row in enumerate(s.splitlines()):
    for ix, c in enumerate(row):
        p = Point(ix, iy)
        for n in p.adjacent4():
            G.add_edge(n, p, weight=int(c))
maxx = len(s.splitlines()[0]) - 1
maxy = len(s.splitlines()) - 1

print(f"Part1: {nx.shortest_path_length(G, source=Point(0, 0), target=Point(maxx, maxy), weight='weight')}")

G = nx.DiGraph()

for xrepeat in range(5):
    for yrepeat in range(5):
        for iy, row in enumerate(s.splitlines()):
            for ix, c in enumerate(row):
                p = Point(ix + xrepeat * (maxx + 1), iy + yrepeat * (maxy + 1))
                for n in p.adjacent4():
                    G.add_edge(n, p, weight=(int(c)+xrepeat+yrepeat-1)%9+1)

# for j in range((maxy+1)*5):
#     for i in range((maxx + 1) * 5):
#         print(G.get_edge_data(Point(i-1, j), Point(i, j))['weight'], end='')
#     print()
print(f"Part2: {nx.shortest_path_length(G, source=Point(0, 0), target=Point((maxx+1)*5-1, (maxy+1)*5-1), weight='weight')}")
# 2153 too low