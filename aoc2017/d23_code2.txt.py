c = b = 99 # 0+1

# 2 to 7
if a != 0:
    b *= 100
    b -= -100000
    c = b
    c -= -17000

# 8 to 10
while True:
    f = 1
    d = 2

    while True: # 10
        e = 2

        while True: #11
            g = d * e - b
            if g == 0:
                f = 0
            e -= 1
            g = e
            g -= b
            if g == 0:  # 19
                break

        d -= -1
        g = d
        g -= b
        if g == 0: # 23 LOOP TO 10
            break

    if f == 0: # 24
        h += 1
    g = b - c
    if g == 0:
        break # EXIT on 29
    b -= -17
