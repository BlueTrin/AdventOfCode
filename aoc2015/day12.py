import re, numbers

s = open("2015_12.txt").read()
total = 0
for m in re.findall(r"([-]*\d+)", s):
    total += int(m)

print(total)

d = eval(s)
def rec(v):
    if isinstance(v, list):
        return sum(rec(x) for x in v)
    elif isinstance(v, dict):
        return 0 if "red" in v.values() else sum(rec(x) for x in v.values())
    elif isinstance(v, (int)):
        return v
    else:
        return 0

print(rec(d))