from aoc_lube import fetch

s = fetch(2017, 15)
print(s)


a0 = int(s.splitlines()[0].split()[-1])
b0 = int(s.splitlines()[1].split()[-1])

print(a0, b0)

def gen(a, b):
    while True:
        a = (a * 16807) % 2147483647
        b = (b * 48271) % 2147483647
        yield a, b

g = gen(a0, b0)

mask = 2**16 - 1
total = 0
for i in range(40000000):
    a, b = next(g)
    if a & mask == b & mask:
        total += 1

print(f"Part1: {total}")

def gena(a):
    while True:
        a = (a * 16807) % 2147483647
        if a % 4 == 0:
            yield a

def genb(b):
    while True:
        b = (b * 48271) % 2147483647
        if b % 8 == 0:
            yield b

total = 0
for i, (a, b) in enumerate(zip(gena(a0), genb(b0))):
    if a & mask == b & mask:
        total += 1
    if i == 5000000:
        break
    if i%100000 == 0:
        print(i)

print(f"Part2: {total}")