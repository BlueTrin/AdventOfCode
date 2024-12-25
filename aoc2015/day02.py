total = 0
ribbon = 0

import itertools
for r in open("2015_02.txt").read().splitlines():
    l, w, h = [int(x) for x in r.split("x")]
    total += 2*l*w + 2*w*h + 2*h*l + min(

        l*w, w*h, h*l
    )
    ribbon += h*l*w + 2* min(x+y for x,y in 
                     itertools.combinations([l, w, h], 2))

print(total)
print(ribbon)