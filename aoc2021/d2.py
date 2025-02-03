from aoc_lube import fetch
import numpy as np

s = fetch(2021, 2)

pos = np.array([0, 0])
for r in s.splitlines():
    di, qty = r.split()
    if di == "forward":
        pos += np.array([0, 1]) * int(qty)
    elif di == "down":
        pos += np.array([1, 0]) * int(qty)
    elif di == "up":
        pos += np.array([-1, 0]) * int(qty)
    assert pos[0] >= 0

print(f"Part1: {pos[1] * pos[0]}")

pos = np.array([0, 0])
aim = np.array([0, 0])
for r in s.splitlines():
    di, qty = r.split()
    if di == "forward":
        pos += np.array([0, 1]) * int(qty)
        pos += aim * int(qty)
    elif di == "down":
        aim += np.array([1, 0]) * int(qty)
    elif di == "up":
        aim += np.array([-1, 0]) * int(qty)

print(f"Part2: {pos[1] * pos[0]}")