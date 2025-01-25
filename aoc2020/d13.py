from aoc_lube import fetch
import math

s = fetch(2020, 13)

print(s)
ts, ids = s.splitlines()
ts = int(ts)
buses = [int(x) for x in ids.split(',') if x != 'x']
shift = {int(x): i for i, x in enumerate(ids.split(',')) if x != 'x'}

min_wait = float('inf')
min_bus = None
for bus in buses:
    if ts % bus == 0:
        min_wait = 0
        min_bus = bus
        break
    else:
        wait = bus - ts % bus
        if wait < min_wait:
            min_wait = wait
            min_bus = bus

print(f"Part1: {min_bus * min_wait}")

# Part2
ts = 0
curr_mod = 1
for bus, i in shift.items():
    if curr_mod == 1:
        curr_mod = bus
        t = i
        continue

    while (ts + i) % bus != 0:
        ts += curr_mod

    curr_mod = math.lcm(curr_mod, bus)

print(f"Part2: {ts}")
# bus 17 -> 32*17 == 544
# bus 37 T+11 -> 37*15 == 555
#
# 629 lcm between 17 and 37
#
# 629 /37
# 17.0
# 629/17
# 37.0
