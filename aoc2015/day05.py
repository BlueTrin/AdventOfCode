s = [r for r in open("2015_05.txt").read().splitlines() if r]


def isnice(r):
    return len([c for c in r if c in "aeiou"]) >= 3 and \
    any(x == y for x, y in zip(r, r[1:])) and \
    all(w not in r for w in ["ab", "cd", "pq", "xy"])
    
def isnice2(r):
    return any((c1+c2) in r[(i+2):] for i, (c1, c2) in enumerate(zip(r, r[1:]))) and \
    any(x == y for x, y in zip(r, r[2:]))
    
print(isnice("ugknbfddgicrmopn"))
print(sum(isnice(r) for r in s))

print(sum(isnice2(r) for r in s))