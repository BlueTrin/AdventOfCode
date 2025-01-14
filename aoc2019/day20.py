import aoc_lube as fetch
from utils.utils import Point, remove_blank_nodes
import networkx as nx
from collections import deque
from pprint import pformat
from heapq import heappop, heappush


s = fetch.fetch(2019, 20)

def find_portal(pt, m2c):
    minx = min(pt.x for pt, c in m2c.items() if c == '#')
    maxx = max(pt.x for pt, c in m2c.items() if c == '#')
    miny = min(pt.y for pt, c in m2c.items() if c == '#')
    maxy = max(pt.y for pt, c in m2c.items() if c == '#')

    for d in pt.adjacent4():
        if m2c[d].isalpha():
            e = [e for e in d.adjacent4() if m2c[e].isalpha()][0]

            pt1, pt2 = sorted([d, e])

            is_outer = e.x < minx or e.x > maxx or e.y < miny or pt.y == maxy

            return f'{m2c[pt1]}{m2c[pt2]}', is_outer
    return None, None


def build_graph(s, part1=True):
    m2c = {}
    outer = set()
    inner = set()

    for y, row in enumerate(s.split('\n')):
        for x, c in enumerate(row):
            m2c[Point(x, y)] = c

    G = nx.Graph()

    for pt, c in m2c.items():
        if c == '.':
            portal, is_outer = find_portal(pt, m2c)
            if portal:
                if portal not in ['AA', 'ZZ']:
                    if is_outer:
                        outer.add(pt)
                    else:
                        inner.add(pt)

                G.add_node(pt, lbl=portal, is_outer=is_outer, weight=1)
            else:
                G.add_node(pt, lbl=c, weight=1)

            for adj in pt.adjacent4():
                if G.has_node(adj) and not G.has_edge(pt, adj):
                    G.add_edge(pt, adj, weight=1)

    remove_blank_nodes(G)

    # add portal
    portals = {}
    for n, d in G.nodes(data=True):
        if d['lbl'] in ['.', 'AA', 'ZZ']:
            continue
        if d['lbl'] not in portals:
            portals[d['lbl']] = []
        portals[d['lbl']].append(n)

    if part1:
        for p, (n1, n2) in portals.items():
            G.add_edge(n1, n2, weight=1)

    portal_map = {}
    portal_names = {}
    for p, (n1, n2) in portals.items():
        portal_map[n1] = n2
        portal_map[n2] = n1
        portal_names[n1] = p
        portal_names[n2] = p

    for n, d in G.nodes(data=True):
        if d['lbl'] == 'AA':
            start = n
        if d['lbl'] == 'ZZ':
            end = n
    return G, start, end, inner, outer, portal_map, portal_names

G, start, end, _, _, _, _= build_graph(s)
print(f"P1: {nx.shortest_path_length(G, start, end, weight='weight')}")

# s = '''             Z L X W       C
#              Z P Q B       K
#   ###########.#.#.#.#######.###############
#   #...#.......#.#.......#.#.......#.#.#...#
#   ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###
#   #.#...#.#.#...#.#.#...#...#...#.#.......#
#   #.###.#######.###.###.#.###.###.#.#######
#   #...#.......#.#...#...#.............#...#
#   #.#########.#######.#.#######.#######.###
#   #...#.#    F       R I       Z    #.#.#.#
#   #.###.#    D       E C       H    #.#.#.#
#   #.#...#                           #...#.#
#   #.###.#                           #.###.#
#   #.#....OA                       WB..#.#..ZH
#   #.###.#                           #.#.#.#
# CJ......#                           #.....#
#   #######                           #######
#   #.#....CK                         #......IC
#   #.###.#                           #.###.#
#   #.....#                           #...#.#
#   ###.###                           #.#.#.#
# XF....#.#                         RF..#.#.#
#   #####.#                           #######
#   #......CJ                       NM..#...#
#   ###.#.#                           #.###.#
# RE....#.#                           #......RF
#   ###.###        X   X       L      #.#.#.#
#   #.....#        F   Q       P      #.#.#.#
#   ###.###########.###.#######.#########.###
#   #.....#...#.....#.......#...#.....#.#...#
#   #####.#.###.#######.#######.###.###.#.#.#
#   #.......#.......#.#.#.#.#...#...#...#.#.#
#   #####.###.#####.#.#.#.#.###.###.#.###.###
#   #.......#.....#.#...#...............#...#
#   #############.#.#.###.###################
#                A O F   N
#                A A D   M                     '''
G, start, end, inner, outer, portal_map, portal_names = build_graph(s, False)
q = []
heappush(q, (0, 0, start, tuple([("AA", 0, 0)])))

min_dist = 1e9
seen = {}
while q:
    level, dist, n, path = heappop(q)



    if n == end and level == 0:
        if dist < min_dist:
            min_dist = min(min_dist, dist)
            print(f"P2: {dist} {pformat(path)}")
        continue
    if seen.get((n, level), min_dist) <= dist:
        continue

    seen[(n, level)] = dist

    for adj in G.adj[n]:
        if adj in outer and level == 0:
            continue

        next_n = portal_map.get(adj, adj)
        if adj in inner:
            next_level = level + 1
            next_dist = dist + G.get_edge_data(n, adj)['weight'] + 1
            next_path = path + ((portal_names[adj], level, next_dist-1), (portal_names[next_n], next_level, next_dist))
        elif adj in outer:
            next_level = level - 1
            next_dist = dist + G.get_edge_data(n, adj)['weight'] + 1
            next_path = path + ((portal_names[adj], level, next_dist-1), (portal_names[next_n], next_level, next_dist))
        else:
            next_level = level
            next_dist = dist + G.get_edge_data(n, adj)['weight']
            next_path = path + (next_n, level, next_dist)

        if seen.get((next_n, next_level), min_dist) > next_dist:
            q.append((next_level, next_dist, next_n, next_path))

    def match_sol(path, sol):
        p_lst = []
        for x in path:
            if not p_lst or p_lst[-1] != x[0]:
                if x[0] == start:
                    lbl = 'AA'
                elif x[0] == end:
                    lbl = 'ZZ'
                else:
                    lbl = x[0]
                p_lst.append(lbl)
        return tuple(p_lst[:len(sol)]) == sol[:len(p_lst)]


    # sol = ('AA',  'XF',  'CK',  'ZH',  'WB',  'IC',  'RF',  'NM',  'LP',  'FD',
    #  'XQ', 'WB', 'ZH', 'CK', 'XF', 'OA', 'CJ', 'RE', 'IC', 'RF', 'NM', 'LP', 'FD',
    #     'XQ', 'WB', 'ZH', 'CK', 'XF', 'OA', 'CJ', 'RE', 'XQ', 'FD', 'ZZ')
    # found_next = False
    # if match_sol(path, sol):
    #     for entry in q:
    #         if match_sol(entry[3], sol):
    #             found_next = True
    #             break
    #     if not found_next:
    #         raise RuntimeError("No next found")

# 1812 too low
print(f"P2: {min_dist}")


