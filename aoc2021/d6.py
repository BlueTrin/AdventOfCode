from aoc_lube import fetch

s = fetch(2021, 6)
print(s)

def sim(s, nbdays):
    f = [int(x) for x in s.split(',')]
    d = {k: 0 for k in range(9)}
    for x in f:
        d[x] += 1

    for _ in range(nbdays):
        for i in range(9):
            d[i-1] = d[i]
        d[8] = d[-1]
        d[6] += d[-1]
        d[-1] = 0

    return sum(d.values())

# assert sim('3,4,3,1,2', 18) == 26

print(f"Part1: {sim(s, 80)}")
print(f"Part2: {sim(s, 256)}")
