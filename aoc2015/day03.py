DIRMAP = {
    '<': -1,
    '>': 1,
    'v': 1j,
    '^': -1j,
}

seen = set()
pos = 0
seen.add(pos)
for s in open("2015_03.txt").read():
    pos += DIRMAP[s]
    seen.add(pos)

print(len(seen))

seen = set()
pos = 0
pos2= 0
seen.add(pos)
inp = open("2015_03.txt").read()
for s, s2 in zip(inp[::2], inp[1::2]):
    pos += DIRMAP[s]
    seen.add(pos)
    pos2 += DIRMAP[s2]
    seen.add(pos2)

print(len(seen))