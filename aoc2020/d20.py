from aoc_lube import fetch
import copy
from collections import defaultdict, deque
from scipy.signal import convolve2d
import numpy as np
from functools import cache

s = fetch(2020, 20)

ex1 = '''Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...'''

def get_tiles(s):
    tiles = {}
    tiles_s = s.split('\n\n')
    for tile_s in tiles_s:
        tile_lines = tile_s.splitlines()
        tile_id = int(tile_lines[0][5:-1])
        tile_rows = tile_lines[1:]
        tiles[tile_id] = np.array([[{'.':0, '#':1}[c] for c in r] for r in tile_rows])

    return tiles

@cache
def apply_transf(tile_id, rotations, flip):
    global TILES
    tile = TILES[tile_id]
    if flip:
        tile = np.flipud(tile)
    if rotations:
        tile = np.rot90(tile, rotations)
    return tile

def apply_transf_imp(tile, rotations, flip):
    if flip:
        tile = np.flipud(tile)
    if rotations:
        tile = np.rot90(tile, rotations)
    return tile


TILES = {}

def solve(s):
    global TILES

    apply_transf.cache_clear()
    TILES = get_tiles(s)

    edge_to_tileid = defaultdict(set)
    for tile_id in TILES:
        for flip in [False, True]:
            for rotations in range(4):
                tile = apply_transf(tile_id, rotations, flip)
                edge_to_tileid[tuple(tile[0,:])].add(tile_id)

    map_size = int(len(TILES) ** 0.5)
    d = deque()
    for tile_id in TILES:
        for flip in [False, True]:
            for rotations in range(4):
                d.append(
                    ((tile_id, rotations, flip),))
    while d:
        history = d.popleft()
        next = len(history)
        next_y = next // map_size
        next_x = next % map_size
        if next_x == 0:
            left_tile = None
        else:
            tileid, rotations, flip = history[next-1]
            left_tile = apply_transf(tileid, rotations, flip)
        if next_y == 0:
            top_tile = None
        else:
            tileid, rotations, flip = history[next-map_size]
            top_tile = apply_transf(tileid, rotations, flip)
        if left_tile is not None:
            left_possibilities = edge_to_tileid[tuple(left_tile[:,-1])] - {x[0] for x in history}
            left_tile_rside = left_tile[:,-1]
        else:
            left_tile_rside = None
            left_possibilities = set(TILES.keys()) - {x[0] for x in history}

        if top_tile is not None:
            top_tile_bside = top_tile[-1,:]
            top_possibilities = edge_to_tileid[tuple(top_tile[-1,:])] - {x[0] for x in history}
        else:
            top_tile_bside = None
            top_possibilities = set(TILES.keys()) - {x[0] for x in history}

        for tile_id in left_possibilities & top_possibilities:
            for flip in [False, True]:
                for rotations in range(4):
                    tile = apply_transf(tile_id, rotations, flip)

                    if left_tile_rside is not None and any(left_tile_rside != tile[:,0]):
                        continue
                    if top_tile_bside is not None and any(top_tile_bside != tile[0,:]):
                        continue

                    next_history = history + ((tile_id, rotations, flip),)
                    if len(next_history) == len(TILES):
                        corners = [0, map_size-1, -map_size, -1]
                        return next_history, np.prod([tile_id for tile_id, _, _ in [next_history[i] for i in corners]])
                    d.append(next_history)
            pass
sol, p1 = solve(ex1)

sol, p1 = solve(s)
print(f"Part 1: {p1}")

l = int(len(sol)**0.5)
grid = np.concatenate([
    np.concatenate([apply_transf(sol[x + l * y][0], sol[x + l * y][1], sol[x + l * y][2])[1:-1, 1:-1] for x in range(l)], axis=1)
    for y in range(l)], axis=0)

monster = '''                  # 
#    ##    ##    ###
 #  #  #  #  #  #   '''
monster = np.array([[{' ':0, '#':1}[c] for c in r] for r in monster.splitlines()])

nb_monsters = 0
for flip in [False, True]:
    for rotations in range(4):
        nb_monsters += len(np.argwhere(convolve2d(grid, apply_transf_imp(monster, rotations, flip), mode='same') == np.sum(monster)))
print(np.sum(grid) - nb_monsters * np.sum(monster))

pass


