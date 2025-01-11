from aoc_lube import fetch
from intcode import Intcode
from utils.utils import Point
import networkx as nx
import logging
from collections import deque

logging.basicConfig(level=logging.DEBUG)

s = fetch(2019, 15)

s = list(map(int, s.strip().split(',')))

c = Intcode(s)

m = {Point(0, 0)}
walls = set()
tgt = None

def next_point_with_unknown(m, walls, pos):
    pts = sorted(m, key=lambda p: pos.manhattan(p))
    for p in pts:
        for n in p.adjacent4():
            if n not in walls and n not in m:
                return p, n-p
    return None

# Only four movement commands are understood: north (1), south (2), west (3), and east (4)
DIR_TO_CMD = {Point(0, -1): 1, Point(0, 1): 2, Point(-1, 0): 3, Point(1, 0): 4}

pos = Point(0, 0)
G = nx.Graph()
G.add_node(pos)
while (dstd:=next_point_with_unknown(m, walls, pos)) is not None:
    logging.debug(f"WALKING FROM {pos} TO {dstd} WHICH HAS UNKNOWN NEIGHBORS")
    dst, d = dstd
    path = nx.shortest_path(G, pos, dst)
    path_d = [p2 - p1 for p1, p2 in zip(path, path[1:])]
    for temp_d in path_d:
        c.add_input(DIR_TO_CMD[temp_d])
        c.run()
        assert c.output.popleft() == 1
        pos += temp_d

    c.add_input(DIR_TO_CMD[d])
    c.run()
    res = c.output.popleft()

    # 0: The repair droid hit a wall. Its position has not changed.
    # 1: The repair droid has moved one step in the requested direction.
    # 2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
    if res == 0:
        walls.add(dst+d)
    elif res in [1, 2]:
        G.add_edge(pos, dst+d)
        pos = dst+d
        m.add(pos)
        if res == 2:
            tgt = pos

print(f"Part 1: {len(nx.shortest_path(G, Point(0, 0), tgt))-1}")

# Part 2
DG = nx.DiGraph()
DG.add_node(tgt)
q = deque([tgt])
while q:
    src = q.popleft()
    for neigh in G.neighbors(src):
        if neigh not in DG:
            q.append(neigh)
            DG.add_edge(src, neigh)

print(f"Part 2: {nx.dag_longest_path_length(DG, tgt)}")


