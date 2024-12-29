from aoc_lube import fetch

s = fetch(2016, 7)

def abba(w):
    for i in range(len(w) - 3):
        if w[i] == w[i + 3] and w[i + 1] == w[i + 2] and w[i] != w[i + 1]:
            return True
    return False

total = 0
for r in s.splitlines():
    words = r.replace("[", "]").split("]")
    has_abba = any(abba(w) for w in words[::2])
    no_abba = not any(abba(w) for w in words[1::2])

    if has_abba and no_abba:
        total += 1

print(f"part 1: {total}")

def findaba(w):
    res = []
    for i in range(len(w) - 2):
        if w[i] == w[i + 2] and w[i] != w[i + 1]:
            res.append(w[i:i + 3])
    return res

def is_ssL(r):
    words = r.replace("[", "]").split("]")
    for w in [aba for word in words[::2] for aba in findaba(word)]:
        bab = f"{w[1]}{w[0]}{w[1]}"
        if any(bab in word for word in words[1::2]):
            return True
    return False

total = 0
for r in s.splitlines():
    if is_ssL(r):
        total += 1
print(f"part 2: {total}")
