from aoc_lube import fetch

s = fetch(2016, 18)

print(s)

def next_row(row):
    res = ""
    for i in range(len(row)):
        l = row[i-1] if i > 0 else '.'
        c = row[i]
        r = row[i+1] if i < len(row)-1 else '.'
        if l == '^' and c == '^' and r == '.':
            res += '^'
        elif l == '.' and c == '^' and r == '^':
            res += '^'
        elif l == '^' and c == '.' and r == '.':
            res +=  '^'
        elif l == '.' and c == '.' and r == '^':
            res += '^'
        else:
            res += '.'
    return res

print(next_row("..^^."))


res = [s]
while len(res) < 40:
    res.append(next_row(res[-1]))

print(sum(r.count('.') for r in res))


res = [s]
while len(res) < 400000:
    res.append(next_row(res[-1]))

print(sum(r.count('.') for r in res))
