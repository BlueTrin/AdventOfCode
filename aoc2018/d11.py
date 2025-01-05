from aoc_lube import fetch

s = fetch(2018, 11)
sn = int(s)

def power(x, y, sn):
    # Find the fuel cell's rack ID, which is its X coordinate plus 10.
    rack_id = x + 10
    # Begin with a power level of the rack ID times the Y coordinate.
    power = rack_id * y
    # Increase the power level by the value of the grid serial number (your puzzle input).
    power += sn
    # Set the power level to itself multiplied by the rack ID.
    power *= rack_id
    # Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
    power = (power // 100) % 10
    # Subtract 5 from the power level.
    power -= 5

    return power


power_levels = {}

for i in range(1, 301):
    for j in range(1, 301):
        power_levels[(i, j)] = power(i, j, sn)

max_power = 0
for i in range(1, 298):
    for j in range(1, 298):
        power = sum(power_levels[(i+k, j+l)] for k in range(3) for l in range(3))
        if power > max_power:
            max_power = power
            max_coord = (i, j)
            print(max_power, max_coord)


max_power = 0
for d in range(1, 301):
    for i in range(1, 301-d):
        for j in range(1, 301-d):
            power = sum(power_levels[(i+k, j+l)] for k in range(d) for l in range(d))
            if power > max_power:
                max_power = power
                max_coord = (i, j)
                print(max_power, max_coord, d)

