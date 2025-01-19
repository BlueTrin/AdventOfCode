from aoc_lube import fetch

s = fetch(2017, 6)

banks = list(map(int, s.split()))

seen = set()

while True:
    if tuple(banks) in seen:
        break
    seen.add(tuple(banks))

    max_index = max(range(len(banks)), key=lambda index: banks[index])
    blocks = banks[max_index]
    banks[max_index] = 0

    for i in range(blocks):
        banks[(max_index + i + 1) % len(banks)] += 1

print(f"Part1: {len(seen)}")

status = tuple(banks)
cycles = 0
while True:

    max_index = max(range(len(banks)), key=lambda index: banks[index])
    blocks = banks[max_index]
    banks[max_index] = 0

    for i in range(blocks):
        banks[(max_index + i + 1) % len(banks)] += 1

    cycles += 1
    if tuple(banks) == status:
        break

print(f"Part2: {status} {cycles}")