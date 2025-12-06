from aoc_lube import fetch
import math
from functools import cache
import numpy as np
from utils.utils import (Point, parse_point, EIGHTDIRS)
import copy
from scipy.ndimage import convolve

s = fetch(2025, 4)

# s = '''..@@.@@@@.
# @@@.@.@.@@
# @@@@@.@.@@
# @.@@@@..@.
# @@.@@@@.@@
# .@@@@@@@.@
# .@.@.@.@@@
# @.@@@.@@@@
# .@@@@@@@@.
# @.@.@@@.@.'''

grid = np.array([list(map('@'.__eq__, line)) for line in s.split('\n')], dtype=bool)
rolls = grid*1

# Any cell which is a roll and has less than 5 rolls in its 3x3 neighbourhood (including itself) is removed
neighbours = convolve(rolls*1, np.ones((3,3), dtype=int), mode='constant')
removed = (neighbours < 5) & rolls
print(f"part 1: {removed}")

part2 = 0
while True:
    part2 += np.sum(removed)

    # we need to remove the rolls which had less than 5 neighbours (including itself)
    rolls = rolls & (neighbours >= 5)
    neighbours = convolve(rolls*1, np.ones((3,3), dtype=int), mode='constant')
    removed = (neighbours < 5) & rolls
    if np.sum(removed) == 0:
        # if we could not remove anymore, we are done
        break

print(f"part 2: {part2}")

