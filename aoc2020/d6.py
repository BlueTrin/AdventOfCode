from aoc_lube import fetch
from functools import reduce

s = fetch(2020, 6)

groups = s.split('\n\n')

num_questions = 0
for group in groups:
    num_questions += len(reduce(lambda a, b: a | b, map(set, group.splitlines())))

print(f"Part1: {num_questions}")



num_questions = 0
for group in groups:
    num_questions += len(reduce(lambda a, b: set.intersection(a, b), map(set, group.splitlines())))

print(f"Part2: {num_questions}")

