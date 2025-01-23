from aoc_lube import fetch

s = fetch(2020, 5)
print(s)

# The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0 through 127).


highest = 0
seats = set()
for r in s.splitlines():
    row = int(r[:7].replace('F', '0').replace('B', '1'), 2)
    col = int(r[7:].replace('L', '0').replace('R', '1'), 2)
    seatid = row*8+col
    highest = max(highest, seatid)

    if seatid in seats:
        raise ValueError(f"Duplicate seatid: {seatid}")
    seats.add(seatid)

print(f"Part1: {highest}")

for i in range(highest):
    if i not in seats and i-1 in seats and i+1 in seats:
        print(f"Part2: {i}")
        break

