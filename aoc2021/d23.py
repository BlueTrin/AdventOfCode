from aoc_lube import fetch
import networkx as nx
from utils import Point
from collections import defaultdict
import functools

from heapq import heappop, heappush

s = fetch(2021, 23)

# uncomment for part 2
s = '\n'.join(s.splitlines()[:3] + ['  #D#C#B#A#  ', '  #D#B#A#C#  '] + s.splitlines()[3:])

print(s)

G = nx.Graph()
pos_map = defaultdict(set)

for i_y, row in enumerate(s.splitlines()):
    for i_x, c in enumerate(row):
        if c not in  {'#', ' '}:
            pt = Point(i_x, i_y)
            G.add_node(pt)
            for n in pt.adjacent4():
                if n in G:
                    G.add_edge(pt, n)
            if c != '.':
                pos_map[c].add(pt)

pos = tuple((l, p) for l in ['A', 'B', 'C', 'D'] for p in pos_map[l])
COST_MAP = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

CORRIDOR = {
    pt
    for pt in G.nodes
    if all(n.y == pt.y for n in G.neighbors(pt))
}


def print_pos(pos):
    min_x = min(p.x for p in G.nodes)
    max_x = max(p.x for p in G.nodes)
    min_y = min(p.y for p in G.nodes)
    max_y = max(p.y for p in G.nodes)
    pos_d = {p: l for l, p in pos}

    for y in range(min_y-1, max_y + 2):
        for x in range(min_x-1, max_x + 2):
            if Point(x, y) in pos_d:
                print(pos_d[Point(x, y)], end='')
            elif Point(x, y) not in G:
                print('#', end='')
            else:
                print('.', end='')
        print()

BURROW = { pt for pt in G.nodes if pt.y > 1 }

CORRECT_BURROW = {'A': 3, 'B': 5, 'C': 7, 'D': 9}

@functools.cache
def shortest_path(source, target):
    return nx.shortest_path(G, source, target)

def min_cost(pos):
    tot_cost = 0
    for l, p in pos:
        tot_cost += len(shortest_path(p, Point(CORRECT_BURROW[l], 2))[1:]) * COST_MAP[l]
    return tot_cost

q = []
curr_cost = 0
heappush(q, (0, curr_cost, pos, tuple()))

seen = {}
lowest_cost = 99999999999999999

while q:
    _len_finished, curr_cost, pos, finished = heappop(q)

    if curr_cost + min_cost(pos) >= lowest_cost:
        continue
    occupied = {pt: l for l, pt in (pos+finished)}

    for ipos, (l, p) in enumerate(pos):
        # try to move each point

        dest_lst = []
        # try to move to corridor or BURROW
        # Amphipods will never move from the hallway into a room unless that room is their destination room and that
        # room contains no amphipods which do not also have that room as their own destination.
        letters_in_burrow = {occupied[pt] for _, pt in pos if pt.x == CORRECT_BURROW[l]}
        if len(letters_in_burrow - {l}) == 0:
            # we can move in the burrow
            burrow_dest = max({pt for pt in BURROW if pt.x == CORRECT_BURROW[l] and pt not in occupied})
            dest_lst.append(burrow_dest)

        if p in BURROW:
            # try to go to corridor
            dest_lst += [pt for pt in CORRIDOR if pt not in occupied]

        if dest_lst:
            for dest in dest_lst:
                # path = nx.shortest_path(G, p, dest)
                path = shortest_path(p, dest)
                assert len(path) >= 2
                if all(pt not in occupied for pt in path[1:]):
                    new_cost = curr_cost + (len(path) - 1) * COST_MAP[l]
                    new_pos = tuple(pos_cpy for i_cpy, pos_cpy in enumerate(pos) if i_cpy != ipos)

                    if dest in BURROW:
                        new_finished = finished + ((l, dest),)
                    else:
                        new_pos += ((l, dest),)
                        new_finished = finished

                    new_pos = tuple(sorted(new_pos))
                    if (new_pos, new_cost) not in seen:
                        if seen.get(new_pos, 99999999999999999) <= new_cost:
                            continue
                        else:
                            seen[new_pos] = new_cost
                        if all(p_new.y > 2 for l_new, p_new in new_pos):
                            print(new_cost)
                            lowest_cost = min(lowest_cost, new_cost)
                        else:
                            if new_cost < lowest_cost:
                                heappush(q, (-len(new_finished), new_cost, new_pos, new_finished))

print(lowest_cost)
# 15365

# Between the first and second lines of text that contain amphipod starting positions, insert the following lines:
#
# '  #D#C#B#A#  '
# '  #D#B#A#C#  ;


