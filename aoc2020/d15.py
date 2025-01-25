from aoc_lube import fetch

s = fetch(2020, 15)

print(s)

nums = list(map(int, s.split(',')))

last = {n: (i, None) for i, n in enumerate(nums)}
turn = len(nums)
print(last, turn)
last_num = nums[-1]
while turn < 2020:
    spoken = last[last_num]
    if spoken[1] is None:
        last_num = 0
    else:
        last_num = spoken[0] - spoken[1]

    last[last_num] = (turn, last.get(last_num, (None, None))[0])
    turn += 1

print(f"Part1: {last_num}")



last = {n: (i, None) for i, n in enumerate(nums)}
turn = len(nums)
print(last, turn)
last_num = nums[-1]
while turn < 30000000:
    spoken = last[last_num]
    if spoken[1] is None:
        last_num = 0
    else:
        last_num = spoken[0] - spoken[1]

    last[last_num] = (turn, last.get(last_num, (None, None))[0])
    turn += 1
print(f"Part2: {last_num} BRUTE FORCE !!!!")