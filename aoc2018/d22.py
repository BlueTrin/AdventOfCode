from aoc_lube import fetch
from functools import cache
import networkx as nx
import itertools

s = fetch(2018, 22)

depth = int(s.splitlines()[0].split(' ')[1])
target = tuple(map(int, s.splitlines()[1].split(' ')[1].split(',')))

# depth = 510
# target = (10, 10)
print(depth, target)

@cache
def geo_index(pt, depth):
    # The region at 0,0 (the mouth of the cave) has a geologic index of 0.
    # The region at the coordinates of the target has a geologic index of 0.
    # If the region's Y coordinate is 0, the geologic index is its X coordinate times 16807.
    # If the region's X coordinate is 0, the geologic index is its Y coordinate times 48271.
    # Otherwise, the region's geologic index is the result of multiplying the erosion levels of the regions at X-1,Y and X,Y-1.
    if pt == (0, 0) or pt == target:
        return 0
    elif pt[1] == 0:
        return pt[0] * 16807
    elif pt[0] == 0:
        return pt[1] * 48271
    else:
        return erosion_level(tuple(map(sum, zip(pt, (-1, 0)))), depth) * erosion_level(tuple(map(sum, zip(pt, (0, -1)))), depth)

def erosion_level(pt, depth):
    return (geo_index(pt, depth) + depth) % 20183

def region_type(pt, depth):
    # If the erosion level modulo 3 is 0, the region's type is rocky.
    # If the erosion level modulo 3 is 1, the region's type is wet.
    # If the erosion level modulo 3 is 2, the region's type is narrow.
    return erosion_level(pt, depth) % 3

# s = ""
# for i in range(target.y + 1):
#     for j in range(target.x + 1):
#         s += '.=|'[region_type(Point(j, i), depth)]
#     s += '\n'
# print(s)

total = 0
for y in range(target[1] + 1):
    if y % 10 == 0:
        print(f"{y}/{target[1]}")
    for x in range(target[0] + 1):
        total += region_type((x, y), depth)
print(total)

# You start at 0,0 (the mouth of the cave) with the torch equipped
G = nx.Graph()
for y in range(target[1] + 100):
    for x in range(target[0] + 100):
        pt = (x, y)
        region = region_type(pt, depth)
        if x==0 and y ==0:
            allowed_tools = range(3)
        else:
            allowed_tools = [tool for tool in range(3)  if tool != region]
        for t1, t2 in itertools.combinations(allowed_tools, 2):
            G.add_edge(pt +  (t1,), pt+ (t2,), weight=7)

        for shift in [(0, 1), (1, 0)]:
            nxt = tuple(map(sum, zip(pt, shift)))
            if nxt[0] >= target[0] + 100 or nxt[1] >= target[1]+100:
                continue
            nx_allowed_tools = [tool for tool in range(3) if tool != region_type(nxt, depth)]
            for t in set.intersection(set(allowed_tools), set(nx_allowed_tools)):
                G.add_edge(pt +(t,), (nxt[0], nxt[1], t), weight=1)

print(nx.dijkstra_path_length(G, (0, 0, 1), target + (1,)))
# 1059 too hgh

# 0 neither - rocky
# 1 torch   - wet
# 2 climbing gear  - narrow

# from networkx.classes.function import path_weight
# print(path_weight(G, [
#     (0, 0, 1),
#     (0, 1, 1),
#     (1, 1, 1),
#     (1, 1, 0),
#     (2, 1, 0),
#     (3, 1, 0),
#     (4, 1, 0),
#     (4, 1, 2),
#     (4, 2, 2),
#     (4, 3, 2),
#     (4, 4, 2),
#     (4, 5, 2),
#     (4, 6, 2),
#     (4, 7, 2),
#     (4, 8, 2),
#     (5, 8, 2),
#     (5, 9, 2),
#     (5, 10, 2),
#     (5, 11, 2),
#
# ], weight="weight"))