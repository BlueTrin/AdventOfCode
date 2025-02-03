from aoc_lube import fetch

s = fetch(2020, 25)

def transform(sub, loop, val=1):
    val = 1
    for _ in range(loop):
        val = (val * sub) % 20201227
    return val

def crack(sub, target):
    val = 1
    loop = 0
    while val != target:
        loop += 1
        val = (val * sub) % 20201227
    return loop

assert transform(7, 8) == 5764801
assert crack(7, 5764801) == 8
assert transform(7, 11) == 17807724

card, door = map(int, s.splitlines())
print(crack(7, card))
print(f"Part1:{transform(door, 8156519)}")
