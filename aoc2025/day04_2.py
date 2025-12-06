from aoc_lube import fetch
import math
from functools import cache
import numpy as np
from utils.utils import (Point, parse_point, EIGHTDIRS)
import copy
from scipy.ndimage import convolve

s = fetch(2025, 4)

s = '''..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.'''

rolls = np.array([list(map('@'.__eq__, line)) for line in s.split('\n')], dtype=bool)

convolve(rolls*1, np.ones((3,3), dtype=int), mode='constant') & rolls
