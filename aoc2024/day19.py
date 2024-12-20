i1 = '''r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
'''


def can_be_built(pattern, chunks, seen=None):
    for chunk in chunks:
        if chunk == pattern:
            return True
        elif pattern.startswith(chunk):
                if can_be_built(pattern[len(chunk):], chunks):
                    return True
    return False


def ccount_built(pattern, chunks, seen=None):
    if seen is None:
        seen = dict()

    total = 0
    if pattern in seen:
        return seen[pattern]

    for chunk in chunks:
        if chunk == pattern:
            seen[pattern] = 1
            total += 1
        elif pattern.startswith(chunk):
            total += ccount_built(pattern[len(chunk):], chunks, seen)
    seen[pattern] = total
    return total

def part1(i1):
    total = 0
    chunks, patterns = i1.split("\n\n")
    chunks = chunks.split(", ")
    patterns = patterns.split("\n")

    for pattern in patterns:
        if can_be_built(pattern, chunks):
            total += 1

    return total


def part2(i1):
    total = 0
    chunks, patterns = i1.split("\n\n")
    chunks = chunks.split(", ")
    patterns = patterns.split("\n")

    for i, pattern in enumerate(patterns):
        if i % 10 == 0:
            print(f"{i}/{len(patterns)}")
        total += ccount_built(pattern, chunks)

    return total

print(part2(i1)) #

import aoc_lube
sol = part2( aoc_lube.fetch(day=19, year=2024)) # 0
print(sol)