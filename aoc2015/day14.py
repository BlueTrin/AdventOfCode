s = open("2015_14.txt").read()

reind = {}
for r in s.splitlines():
    t = r.split(" ")

    reind[t[0]] = (int(t[3]), int(t[6]), int(t[-2]))

print(reind)

maxdst = 0

for r, (v, rv, pa) in reind.items():
    dst = 2503 // (rv+pa) * v * rv + min(
        2503 % (rv+pa), rv) * v 
    print(dst, 2503 // (rv+pa), 2503 % (rv+pa))

    maxdst = max(dst, maxdst)

print(maxdst)

total = [0] * len(reind)
for t in range(1, 2504):
    dst = [t // (rv+pa) * v * rv + min(
        t % (rv+pa), rv) * v
           for r, (v, rv, pa) in reind.items()]
    total[dst.index(max(dst))] += 1

print(total)