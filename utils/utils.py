import logging
import time
from typing import Dict, List, Tuple, Set
from collections import namedtuple
import math
import numpy as np
import itertools
import numbers


class Point(namedtuple('Point',['x', 'y'])):
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y )

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def adjacent4(self):
        return [self + d for d in FOURDIRS]

    def adjacent8(self):
        return [self + d for d in EIGHTDIRS]

    def rotate(self, degrees):
        rad = math.radians(degrees)
        x = self.x * math.cos(rad) - self.y * math.sin(rad)
        y = self.x * math.sin(rad) + self.y * math.cos(rad)
        return Point(round(x), round(y))

N = Point(0, -1)
S = Point(0, 1)
W = Point(-1, 0)
E = Point(1, 0)

FOURDIRS = [N, S, E, W]

NW = N + W
NE = N + E
SW = S + W
SE = S + E

EIGHTDIRS = [N, S, E, W, NW, NE, SW, SE]

class Point3D(namedtuple('Point',['x', 'y', 'z'])):
    def __add__(self, other):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Point3D(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        if isinstance(other, numbers.Number):
            return Point3D(self.x / other, self.y / other, self.z / other)
        else:
            raise NotImplementedError()

    def manhattan(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


def map_dst(start: complex, allowed: Set[complex]) -> Dict[complex, int]:
    '''
    Does a fill algo and returns a map (coord -> distance) of all allowed coords from start
    '''
    dst_map = {start: 0}
    boundary = dst_map
    has_written = True
    curr_dst = 0
    while has_written:
        has_written = False
        curr_dst += 1
        new_boundary = {}
        for c in boundary:
            for d in FOURDIRS:
                dst = c+d
                if dst in allowed and dst not in dst_map:
                    new_boundary[dst] = curr_dst
                    has_written = True
        dst_map.update(new_boundary)
        boundary = new_boundary
    return dst_map

def aoc_timer(part=0, day=0, year=0):
    part = {1: 'one', 2: 'two'}.get(part)
    prepend = ''
    if year:
        prepend += '%s.' % year
    if day:
        prepend += '%s ' % day
    if part:
        prepend += 'part %s: ' % part
    def decorator(func):
        def wrapper(*a, **kw):
            try:
                start = time.perf_counter()
                result = func(*a, **kw)
                delta = (time.perf_counter() - start) * 1000
                if not prepend:
                    print(f'finished {func.__name__} in {delta:.4f} ms')
                else:
                    print(f'{prepend}{result} ({delta:.4f} ms)')
            except Exception as e:
                logging.exception(f'exception when solving {prepend}: {e}')
            else:
                return result
        return wrapper
    return decorator

def parse_space_separated(txt_input_str):
    '''
    >>> parse_space_separated("""1 2 3
    ... 4 5 6
    ... 7 8 9""")

    :param txt_input_str:
    :return:
    '''
    res = None
    for i_y, r in enumerate([r for r in txt_input_str.splitlines() if r]):
        for i_x, c in enumerate(r.split()):
            if res is None:
                res = [[] for i in  range(len(r.split()))]
            res[i_x].append(int(c))
    return res

def parse_complex(txt_input: str) -> Tuple[Dict[complex, str], Dict[str, Set[complex]], Tuple[int, int]]:
    '''
    Read input into complex coordinates
    >>> ex_txt_input = """.X.X
    ... ...
    ... .OO.
    ... """
    >>> co_to_c, c_to_cos, lens = parse_complex(ex_txt_input)

    :param txt_input:
    :return:
     (coords_to_char, char_to_coordsset, max_coords):
      -
    '''

    coords_to_char = {}
    char_to_coordsset = {}

    for i_y, r in enumerate(txt_input.split("\n")):
        if r:
            for i_x, c in enumerate(r):
                pt = i_x + i_y * 1j

                coords_to_char[pt] = c

                if c not in char_to_coordsset:
                    char_to_coordsset[c] = set()
                char_to_coordsset[c].add(pt)

    max_coords = (
        len(txt_input.split("\n")[0]),
        len([x for x in txt_input.split("\n") if x]))

    return coords_to_char, char_to_coordsset, max_coords


def rotation_x_3d(vec, degrees):
    rad = math.radians(degrees)
    rot = np.array([[ 1, 0 ,0],
                     [ 0, math.cos(rad) ,-math.sin(rad)],
                     [ 0, math.sin(rad) ,math.cos(rad)]])
    return vec @ rot

def rotation_y_3d(vec, degrees):
    rad = math.radians(degrees)
    rot = np.array([[ math.cos(rad), 0 ,math.sin(rad)],
                     [ 0,  1, 0],
                     [ -math.sin(rad), 0 ,math.cos(rad)]])
    return vec @ rot

def rotation_z_3d(vec, degrees):
    rad = math.radians(degrees)
    rot = np.array([[math.cos(rad) ,-math.sin(rad), 0],
                     [ math.sin(rad) ,math.cos(rad), 0],
                     [0, 0, 1],
                     ])
    return vec @ rot

# if __name__ == '__main__':
#     from adventofcode.inputs import get_input
#     txt_input = get_input(8, year=aoc2024)
#     coords_to_char, char_to_coordsset, max_coords = parse_complex(txt_input)
#     pass


# SIMPLIFY EDGES BY REMOVING ALL BLANK NODES
def remove_blank_nodes(G):
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


def primes(n):
    """ Returns  a list of primes < n """
    sieve = [True] * n
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i]:
            sieve[i*i::2*i]=[False]*((n-i*i-1)//(2*i)+1)
    return [2] + [i for i in range(3,n,2) if sieve[i]]