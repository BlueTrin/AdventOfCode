from aoc_lube import fetch

s = fetch(2016, 16)

def dragon(a):
    b = ''.join(['0' if x == '1' else '1' for x in a[::-1]])
    return f'{a}0{b}'

assert dragon('1') =='100'
assert dragon('111100001010') == '1111000010100101011110000'

l = 272

while len(s) < l:
    s = dragon(s)

s = s[:l]
chk = ''.join(str(int(c1 == c2)) for c1, c2 in zip(s[::2], s[1::2]))
while len(chk) % 2 == 0:
    chk = ''.join(str(int(c1 == c2)) for c1, c2 in zip(chk[::2], chk[1::2]))

print(chk)


s = fetch(2016, 16)

l = 35651584

while len(s) < l:
    s = dragon(s)

s = s[:l]
chk = ''.join(str(int(c1 == c2)) for c1, c2 in zip(s[::2], s[1::2]))
while len(chk) % 2 == 0:
    chk = ''.join(str(int(c1 == c2)) for c1, c2 in zip(chk[::2], chk[1::2]))

print(chk)
