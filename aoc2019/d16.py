from aoc_lube import fetch

s = fetch(2019, 16)

v = list(map(int, s.strip()))
print(v)

def gen_pattern(n):
    first = True
    while True:
        base = [0, 1, 0, -1]
        for b in base:
            for i in range(n):
                if first:
                    first = False
                    continue
                yield b

def phase(v):
    res = []
    for i in range(len(v)):
        pattern = gen_pattern(i + 1)

        res.append(abs(sum(c * next(pattern) for c in v)) % 10)
    return res

def nphases(v, n):
    for i in range(n):
        v = phase(v)
    return v

assert phase(list(map(int, '12345678'))) == [4, 8, 2, 2, 6, 1, 5, 8]


# print("Part1: ", ''.join(map(str, nphases(v, 100)[:8])))
#
shift = int(''.join(map(str, v[:7])))
print(f"shift={shift:,} len(v)={len(v)*10000:,}")

# the pattern he gave makes it that for second half, the digits are a cumulative sum of the digits from the end
# but modulo 10

def phase_rev(s):
    res = []
    for i in range(len(s) - 1, -1, -1):
        res.append((s[i] + (res[-1] if res else 0)) % 10)
    return res[::-1]

v = v * 10000

v = v[shift:]
for i in range(100):
    v = phase_rev(v)

print("Part2: ", ''.join(map(str, v[:8])))
