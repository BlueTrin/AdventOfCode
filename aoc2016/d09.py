from aoc_lube import fetch
import re
s = fetch(2016, 9)

def decompress(s, part2=False):
    out = ""
    curr = 0
    while curr < len(s):
        try:
            m = next(re.finditer(r"\((\d+)x(\d+)\)", s[curr:]))
        except StopIteration:
            out += s[curr:]
            break
        out += s[curr:curr+m.start()] + s[curr+m.end():curr+m.end()+int(m.group(1))] * int(m.group(2))
        curr += m.end() + int(m.group(1))

    return out
    pass


assert len(decompress("ADVENT")) == 6
assert len(decompress("A(1x5)BC")) == 7
assert len(decompress("(3x3)XYZ")) == 9
assert len(decompress("A(2x2)BCD(2x2)EFG")) == 11
assert len(decompress("(6x1)(1x3)A")) == 6
assert len(decompress("X(8x2)(3x3)ABCY")) == 18


total = 0
for r in s.splitlines():
    if not r:
        continue
    total += len(decompress(r))

print(total)

def decompress_len(s):
    out = 0
    curr = 0
    while curr < len(s):
        try:
            m = next(re.finditer(r"\((\d+)x(\d+)\)", s[curr:]))
        except StopIteration:
            out += len(s[curr:])
            break
        out += len(s[curr:curr+m.start()]) + int(m.group(2)) * decompress_len(s[curr+m.end():curr+m.end()+int(m.group(1))])
        curr += m.end() + int(m.group(1))

    return out


assert decompress_len("(3x3)XYZ") == 9
assert decompress_len("X(8x2)(3x3)ABCY") == 20
assert decompress_len("(27x12)(20x12)(13x14)(7x10)(1x12)A") == 241920
assert decompress_len("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN") == 445

total = 0
for r in s.splitlines():
    if not r:
        continue
    total += decompress_len(r)

print(total)