from aoc_lube import fetch
from collections import deque
from functools import cache


s = fetch(2020, 10)

nums = list(map(int, s.splitlines()))
print(nums)
assert(len(set(nums)) == len(nums))

nums = set(nums)

ch = [0] + sorted(nums) + [max(nums) + 3]
diffs = [p2-p1 for p1, p2 in zip(ch, ch[1:])]

print(f"par1: {diffs.count(1) * diffs.count(3)}")

d = deque()
d.append(0)

@cache
def count_ways(i, nums):
    count = 0
    for x in nums:
        if x > i and x <= i + 3:
            count += count_ways(x, nums)
    return count or 1

print(f"part2: {count_ways(0, tuple(nums))}")
