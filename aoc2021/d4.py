from aoc_lube import fetch
import numpy as np
from collections import deque


s = fetch(2021, 4)

seq_s, *grids_s = s.split("\n\n")

seq = tuple(int(x) for x in seq_s.split(','))

grids = []
for grid_s in grids_s:
    grid = np.array([[int(x) for x in row.split()] for row in grid_s.splitlines()])
    grids.append(grid)

matches = [np.full_like(grid, 0) for grid in grids]

d = deque(seq)
p1 = None
won = set()
while d:
    n = d.popleft()
    for igrid, (grid, match) in enumerate(zip(grids, matches)):
        if igrid in won:
            continue
        grid_match = (grid == n)
        match |= grid_match
        for i, j in np.transpose(np.where(grid_match)):
            if all(match[i, :]) or all(match[:, j]):
                won.add(igrid)
                if p1 is None:
                    p1 = sum(grid[match == 0]) * n
                    print(f"part1: {p1}")
                p2 = sum(grid[match == 0]) * n

    if len(won) == len(grids):
        print(f"part2: {p2}")
        break
