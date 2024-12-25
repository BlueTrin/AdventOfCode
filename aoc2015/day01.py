s = open("2015_01.txt").read()
print(s.count("(")-s.count(")"))

lev = 0
for i, c in enumerate(s):
    lev += 1 if c == "(" else -1
    if lev <0:
        print(i+1)
        break