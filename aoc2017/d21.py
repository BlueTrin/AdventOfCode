from aoc_lube import fetch
import itertools

s = fetch(2017, 21)

def flip(grid, vflip, hflip):
    if vflip:
        grid = grid[::-1]
    if hflip:
        grid = tuple(r[::-1] for r in grid)
    return grid

def rotate(grid, n):
    for _ in range(n):
        grid = tuple(''.join(r[i] for r in grid)[::-1] for i in range(len(grid)))
    return grid

assert flip(['123','456','789'],True,True) == rotate(['123','456','789'],2)

rules = {}
for r in s.splitlines():
    a, b = r.split(' => ')

    in_rows = a.split('/')
    out_rows = b.split('/')

    for vrot, hrot in itertools.product([True, False], repeat=2):
        for rot in range(4):
            in_rows_ = rotate(in_rows, rot)
        in_rows_ = flip(in_rows, vrot, hrot)
        in_rows_ = tuple(in_rows_)

        rules[in_rows_] = out_rows

        for _ in range(3):
            in_rows_ = rotate(in_rows_, 1)
            if in_rows_ not in rules:
                rules[in_rows_] = out_rows
            else:
                assert rules[in_rows_] == out_rows


start = '''.#.
..#
###'''.splitlines()


pass



def get_subgrid(grid, x, y, div):
    return tuple([r[x:x+div] for r in grid[y:y+div]])

def set_subgrid(grid, x, y, div, subgrid):
    for i, r in enumerate(subgrid):
        grid[y+i] = grid[y+i][:x] + r + grid[y+i][x+div:]

def enhance(start, rules):
    if len(start) % 2 == 0:
        div = 2
    elif len(start) % 3 == 0:
        div = 3
    else:
        raise ValueError()

    new_grid = ['X' * (len(start) // div * (div+1))] * (len(start) // div * (div+1))
    for y in range(0, len(start), div):
        for x in range(0, len(start), div):
            subgrid = get_subgrid(start, x, y, div)
            new_subgrid = rules[subgrid]
            set_subgrid(new_grid, x//div*(div+1), y//div*(div+1), div+1, new_subgrid)
    assert all('X' not in r for r in new_grid)
    return new_grid

for i in range(5):
    start = enhance(start, rules)

print(f"Part1: {sum(r.count('#') for r in start)}")


for i in range(13):
    start = enhance(start, rules)
print(f"Part2: {sum(r.count('#') for r in start)}")
