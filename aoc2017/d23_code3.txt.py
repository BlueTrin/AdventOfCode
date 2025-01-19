a=b=c=d=e=f=g=h=0
a=1
#b = 109900
c = 126900

# 8 to 10
for b in range(109900, c+1, 17):
    f = 1
    for d in range(2, b+1):
        for e in range(2, b+1):
            if b == d * e:
                f = 0
        d -= -1

    if f == 0: # 24
        h += 1

