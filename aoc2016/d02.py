from aoc_lube import fetch

s = fetch(2016, 2)

keypad_s = '''123
456
789'''

keypad = {}
for y, r in enumerate(keypad_s.split('\n')):
    for x, c in enumerate(r):
        keypad[x + y*1j] = c

pos = 1 + 1j
for r in s.splitlines():
    for c in r:
        if c == 'U' and pos - 1j in keypad:
            pos -= 1j
        elif c == 'D' and pos + 1j in keypad:
            pos += 1j
        elif c == 'L' and pos - 1 in keypad:
            pos -= 1
        elif c == 'R' and pos + 1 in keypad:
            pos += 1
    print(keypad[pos], end='')

keypad_s = '''  1
 234
56789
 ABC
  D'''
keypad = {}
for y, r in enumerate(keypad_s.split('\n')):
    for x, c in enumerate(r):
        if c != ' ':
            keypad[x + y*1j] = c

print("part2")
pos = 1 + 1j
for r in s.splitlines():
    for c in r:
        if c == 'U' and pos - 1j in keypad:
            pos -= 1j
        elif c == 'D' and pos + 1j in keypad:
            pos += 1j
        elif c == 'L' and pos - 1 in keypad:
            pos -= 1
        elif c == 'R' and pos + 1 in keypad:
            pos += 1
    print(keypad[pos], end='')
