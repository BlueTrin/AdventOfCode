import networkx as nx
from utils.utils import Point
from aoc_lube import fetch

s = fetch(2017, 11)



def build_graoh(s):
    directions = s.split(',')
    pos = Point(0, 0)
    G= nx.Graph()
    for d in directions:
        prev = pos
        if d == 'n':
            pos += Point(0, -2)
        elif d == 's':
            pos += Point(0, 2)
        elif d == 'ne':
            pos += Point(1, -1)
        elif d == 'sw':
            pos += Point(-1, 1)
        elif d == 'nw':
            pos += Point(-1, -1)
        elif d == 'se':
            pos += Point(1, 1)

        G.add_edge(prev, pos)
    return G, pos

G, pos = build_graoh(s)
def dst(pt):
    steps = 0
    #diag steps
    steps += min(abs(pt.x), abs(pt.y))
    #straight steps
    x = abs(pt.x) - abs(steps)
    y = abs(pt.y) - abs(steps)

    # south and north you move by 2 but sideways you move by 1
    steps += abs(y) //2 + abs(x)
    return steps

print(f"Part1: {dst(pos)}")

print(f"Part2: {max([dst(n) for n in G.nodes])}")
