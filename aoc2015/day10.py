s = "1113222113"

import itertools

for i in range(50):
    n = []
    for l, g in itertools.groupby(s):
        # n += str(len(list(g))) + str(l)
        n += [len(list(g)), int(l)]
        # print(n)
    s = n

# print(s)
print(len(s))
