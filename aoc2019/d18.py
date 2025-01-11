#!../.venv/bin/python
from aoc_lube import fetch
import math
import networkx as nx
from utils.utils import Point
from collections import defaultdict
import time
from blessed import Terminal
import sys
import colorsys
import itertools
import matplotlib.pyplot as plt
import matplotlib
import platform
import logging
import random
from collections import deque
import time

logging.basicConfig(format='%(asctime)s %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if platform.system() == 'Darwin':
    matplotlib.use('MacOSX')

s = fetch(2019, 18)

def scale_255(val): return int(round(val * 255))

def rgb_at_xy(term, x, y, t, h, w):
    if h or w is None:
        h, w = term.height, term.width
    hue = 4.0 + (
        math.sin(x / 16.0)
        + math.sin(y / 32.0)
        + math.sin(math.sqrt(
            ((x - w / 2.0) * (x - w / 2.0) +
             (y - h / 2.0) * (y - h / 2.0))
        ) / 8.0 + t * 3)
    ) + math.sin(math.sqrt((x * x + y * y)) / 8.0)
    saturation = y / h
    lightness = x / w
    return tuple(map(scale_255, colorsys.hsv_to_rgb(hue / 8.0, saturation, lightness)))

#print(s)

start_time = time.perf_counter()

G = nx.Graph()
m = {}
c2m = defaultdict(set)

for iy, r in enumerate(s.splitlines()):
    for ix, c in enumerate(r):
        if c == '#':
            continue
        m[Point(ix, iy)] = c
        c2m[c].add(Point(ix, iy))
        G.add_node(Point(ix, iy), lbl=c, colour=('red' if c.isupper() else 'green') if c.isalpha() else 'blue')

for p, c in m.items():
    for adj in p.adjacent4():
        if adj in m:
            G.add_edge(p, adj, weight=1)

print(f"start: {c2m['@']}")
start = next(iter(c2m['@']))
keys_n_doors = c2m.keys() - {'.', '#', '@'}
keys = {k for k in keys_n_doors if k.islower()}
doors = {d for d in keys_n_doors if d.isupper()}
print(keys)
print(doors)

def print_maze_colours(m):
    # local

    term = Terminal()

    x, y, xs, ys = 2, 2, 0.4, 0.3
    with term.cbreak(), term.hidden_cursor(), term.fullscreen():
        # clear the screen
        # print(term.home + term.black_on_grey + term.clear)

        while True:
            minx, maxx = min(m.keys(), key=lambda p: p.x).x-1, max(m.keys(), key=lambda p: p.x).x+1
            miny, maxy = min(m.keys(), key=lambda p: p.y).y-1, max(m.keys(), key=lambda p: p.y).y+1
            for iy in range(miny, maxy+1):
                for ix in range(minx, maxx+1):

                    c = m.get(Point(ix, iy))
                    if c is None:
                        print(term.on_color_rgb(*rgb_at_xy(term, ix, iy, time.time(), maxx, maxy))+' ', end='')
                    else:
                        if c == '.':
                            c = ' '
                        print(term.white_on_black + c, end='')
                print(term.normal)

            print(term.move(0, 0))
            sys.stdout.flush()
            time.sleep(0.05)

def print_maze(m):
    term = Terminal()

    minx, maxx = min(m.keys(), key=lambda p: p.x).x - 1, max(m.keys(), key=lambda p: p.x).x + 1
    miny, maxy = min(m.keys(), key=lambda p: p.y).y - 1, max(m.keys(), key=lambda p: p.y).y + 1
    with term.cbreak(), term.hidden_cursor(), term.fullscreen():
        for iy in range(miny, maxy + 1):
            for ix in range(minx, maxx + 1):
                c = m.get(Point(ix, iy))
                if c == '.':
                    c = ' '
                elif c is None:
                    c = term.black_on_white + '#'
                print(c, end='')
            print()

print_maze(m)

ORIG_G = G.copy()

# SIMPLIFY EDGES BY REMOVING ALL BLANK NODES
remove_edge = True
while remove_edge:
    remove_edge = False
    nodes_to_remove = [(n, d) for n, d in G.nodes(data=True) if d['lbl'] == '.']
    for n, d in nodes_to_remove:
        neighbours = list(G.adj[n])
        for n1, n2 in itertools.combinations(neighbours, 2):
            # logger.debug(f"  ** Link {n1} and {n2} via {n}: {G.get_edge_data(n, n1)['weight']} + {G.get_edge_data(n, n2)['weight']}")
            new_weight = G.get_edge_data(n, n1)['weight'] + G.get_edge_data(n, n2)['weight']
            if not G.has_edge(n1, n2) or G.get_edge_data(n1, n2)['weight'] > new_weight:
                G.add_edge(n1, n2, weight=new_weight)
        for n1 in neighbours:
            G.remove_edge(n, n1)
        G.remove_node(n)
        remove_edge = True

# SANITY CHECK
for n1, n2 in random.choices(list(G.edges), k=10):
    assert nx.shortest_path_length(ORIG_G, n1, n2) == G.get_edge_data(n1, n2)['weight']


# DISPLAY GRAPH
def display_graph(G):
    pos = nx.spring_layout(G)

    # nx.draw_networkx_nodes(G, pos)
    # nx.draw_networkx_labels(G, pos)
    # nx.draw_networkx_edges(G, pos, edge_color='r', arrows = True)

    fig = plt.figure(figsize=(50,50))
    pos = nx.bfs_layout(G, start=start)
    color_map = [d['colour'] for n, d in G.nodes(data=True)]
    node_labels = {n: d['lbl'] for n, d in G.nodes(data=True)}
    nx.draw(G, pos=pos, with_labels=True, node_color=color_map, labels=node_labels, font_size=8)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    plt.show()

#display_graph(G)

# position, keys, distance so far
d = deque([(start, frozenset(), 0)])
seen = dict()
min_dist = 9999999999999

while d:
    pos, keys_sofar, dist = d.popleft()
    if seen.get((pos, keys_sofar), min_dist) <= dist:
        continue
    seen[(pos, keys_sofar)] = dist
    if keys_sofar == keys:
#        print(f"Part 1: {dist}")
        min_dist = dist
        continue

    for n in G.adj[pos]:
        if G.nodes[n]['lbl'] in doors and G.nodes[n]['lbl'].lower() not in keys_sofar:
            continue
        if G.nodes[n]['lbl'] in keys and G.nodes[n]['lbl'] not in keys_sofar:
            next_keys = keys_sofar | {G.nodes[n]['lbl']}
        else:
            next_keys = keys_sofar

        if seen.get((n, next_keys), min_dist) > dist + G.get_edge_data(pos, n)['weight']:
            d.append((n, next_keys, dist + G.get_edge_data(pos, n)['weight']))
end_time = time.perf_counter()

print(f"Part 1: {min_dist} in {end_time-start_time:.2f} seconds")
