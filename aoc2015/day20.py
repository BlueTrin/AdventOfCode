from math import sqrt


res = [0] * 1000000

for i in range(1, 1000000):
    for j in range(i, 1000000, i):
        res[j] += i * 10

for i, r in enumerate(res):
    if r >= 33100000:
        print(i)
        break

# part 2
res = [0] * 1000000

for i in range(1, 1000000):
    for j in range(i, min(1000000, i*50), i):
        res[j] += i * 11

for i, r in enumerate(res):
    if r >= 33100000:
        print(i)
        break