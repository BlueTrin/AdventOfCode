from aoc_lube import fetch
from collections import deque

s = fetch(2017, 17)
print(f"input: {s}")
steps = int(s)

def spinlock(steps, n=2017):
    l = deque([0])
    for i in range(1, n + 1):
        l.rotate(-steps)
        l.append(i)
    return l

l = spinlock(3)
assert l[(l.index(2017) + 1)%len(l)] == 638

l = spinlock(steps)
assert l[(l.index(2017) + 1)%len(l)]== 419
print(f"Part1: {l[(l.index(2017) + 1)%len(l)]}")

def fast_part2(steps, n=50000000):
    # we don't need to keep track of the list, just the value after 0
    pos = 0
    for i in range(1, n + 1):
        pos = (pos + steps) % i + 1
        if pos == 1:
            result = i
    return result

print(f"Part2: {fast_part2(steps)}")

print("Now, let's try a different approach ... BRUTE FORCE!!!")
l = spinlock(steps, n=50000000)
assert 50000000 in l
assert 50000001 not in l

print(f"Part2: {l[(l.index(0) + 1)%len(l)]}")
pass