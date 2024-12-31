from aoc_lube import fetch
from collections import deque

s = fetch(2016, 19)

print(s)

elves = [i for i in range(1, int(s)+1)]
while len(elves) > 1:
    elves = elves[::2][len(elves) % 2:]

print("part1:", elves[0])


i = 1

while i * 3 < int(s):
    i *= 3

print(int(s) - i)

