import re


s = open("2015_08.txt").read().splitlines()


def part1(lines):
    total = 0
    for r in lines:
        if not r:
            continue
        a = r.strip()[1:-1]
        subtotal = 2
        for m in re.finditer(r'(?P<dd>\\")|(?P<ds>\\\\)|(?P<hex>\\x[\d|a-f|A-F]{2})', a):
            if m.groupdict()['dd'] or m.groupdict()['ds']:
                subtotal += 1
            elif m.groupdict()['hex']:
                subtotal += 3
        print(f"after {r} total={subtotal}")
        total += subtotal
        check = len(r) - len(eval(r))
        if check != subtotal:
            print(f"{check} != {subtotal}")
            print(f"`{r}`")
            raise RuntimeError()
    return total


def part2(lines):
    total = 0
    for r in lines:
        if not r:
            continue
        subtotal = 2 + r.count('"') + r.count('\\')
        total += subtotal
    return total


print(part1(r'''""
"abc"
"aaa\"aaa"
"\x27"
"wlsdw\xb3dmiy\\od"
'''.splitlines()))

print(part1(s))

print(part2(s))