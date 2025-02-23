from aoc_lube import fetch

def sgn(x):
    if x == 0:
        return 0
    elif x < 0:
        return -1
    else:
        return 1

s = fetch(2021, 17)
print(s)
tgt_x, tgt_y = [tuple(map(int, x.split('..'))) for x in s.replace('target area: ', '').replace('x=', '').replace('y=', '').split(', ')]
print(tgt_x, tgt_y)

# find the smallest x that hits the target area
guess_dx = 0
end_x = 0
while end_x < tgt_x[0]:
    guess_dx += 1
    end_x += guess_dx

def hit_target(start_dx, start_dy, tgt_x, tgt_y):
    x = y = 0
    max_y = -999999999
    dx, dy = start_dx, start_dy
    while x <= tgt_x[1] and y >= tgt_y[0]:
        x += dx
        y += dy
        max_y = max(max_y, y)

        dx -= sgn(dx)
        dy -= 1
        if tgt_x[0] <= x <= tgt_x[1] and tgt_y[0] <= y <= tgt_y[1]:
            return True, max_y

    return False, max_y


max_y = -999999999
p2 = 0
for start_dx in range(guess_dx, tgt_x[1] + 1):
    for start_dy in range(-100, 100):
        if (res:=hit_target(start_dx, start_dy, tgt_x, tgt_y))[0]:
            max_y = max(max_y, res[1])
            p2 += 1
print(f"Part1: {max_y}")
# 253 too low
print(f"Part2: {p2}")
# 158 too low
#1477