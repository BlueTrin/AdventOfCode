import hashlib
from aoc_lube import fetch

s = fetch(2016, 5)

def code(part2=False):
    i = 0
    if part2:
        sol = ["_"] * 8
    else:
        sol = ""
    while True:
        m = hashlib.md5()
        text = f"reyedfim{i}"
        # text = f"abc{i}"
        m.update(text.encode('UTF-8'))
        hash = m.hexdigest()
        if hash.startswith("00000"):
            if part2:
                if hash[5] in "01234567" and sol[int(hash[5])] == "_":
                    sol[int(hash[5])] = hash[6]
                    print(i, "".join(sol))
                    if "_" not in sol:
                        break
            else:
                sol += hash[5]
                print(i, sol)
                if len(sol) == 8:
                    break

        i += 1

print(code())
print(code(True))
