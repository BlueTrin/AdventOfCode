from aoc_lube import fetch
from functools import reduce


def knot_hash(lengths, l=256, rounds=1):
    lst = list(range(l))
    pos = 0
    skip = 0

    # Reverse the order of that length of elements in the list, starting with the element at the current position.
    # Move the current position forward by that length plus the skip size.
    # Increase the skip size by one.
    for _ in range(rounds):
        for length in lengths:
            for i in range(length // 2):
                a = (pos + i) % l
                b = (pos + length - i - 1) % l
                lst[a], lst[b] = lst[b], lst[a]

            pos += length + skip
            skip += 1
    return lst

def knot_hash2(s):
    lengths = [ord(c) for c in s]
    lengths.extend([17, 31, 73, 47, 23])
    part2 = knot_hash(lengths, rounds=64)

    dense_hash = 0
    for i in range(0, 256, 16):
        dense_hash = dense_hash << 8
        elt = reduce(lambda a, b: a ^ b, part2[i:i+16])
        assert 0 <= elt < 256
        dense_hash += elt
    return dense_hash

if __name__ == '__main__':
    s = fetch(2017, 10)
    print(s)
    lengths = list(map(int, s.strip().split(',')))
    part1 = knot_hash(lengths)
    print(f"Part1: {part1[0] * part1[1]}")

    dense_hash = knot_hash2(s)
    print(f"Part2: {dense_hash:x}")
    assert dense_hash == int("c500ffe015c83b60fad2e4b7d59dabc4", 16)
