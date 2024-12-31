from aoc_lube import fetch

s = fetch(2016, 21)

print(s)

def rotate(s, n):
    n = n % len(s)
    return s[n:] + s[:n]

def move(password, a, b):
    temp = password[:a] + password[a + 1:]
    password = temp[:b] + password[a] + temp[b:]
    return password


password = "abcdefgh"
def exec(password, cmd_str, debug=False, reverse=False):
    orig_len = len(password)

    instructions = cmd_str.splitlines()
    if reverse:
        instructions = instructions[::-1]
    for r in instructions:
        if r is None:
            continue

        if debug:
            print(f"Executing {r}, password={password}")
        cmd, *args = r.split()
        if cmd == "rotate":
            if args[0] == "right":
                n = -int(args[1])
                if reverse:
                    n = -n
            elif args[0] == "left":
                n = int(args[1])
                if reverse:
                    n = -n
            elif args[0] == "based":
                idx = password.index(args[-1])
                if reverse:
                    poss = [x for x in range(len(password)) if rotate(rotate(password, idx-x), -(1 + x + (1 if x >= 4 else 0))) == password]
                    if len(poss) != 1:
                        raise RuntimeError("Invalid input")
                    password = rotate(password, idx-poss[0])
                    continue
                else:
                    n = -(1 + idx + (1 if idx >= 4 else 0))
            else:
                raise RuntimeError("Invalid input")


            password = rotate(password, n)
        elif cmd == "swap":
            if args[0] == "position":
                a, b = sorted((int(args[1]), int(args[4])))
                password = password[:a] + password[b] + password[a+1:b] + password[a] + password[b+1:]

            elif args[0] == "letter":
                a, b = args[1], args[4]
                password = password.replace(a, 'x').replace(b, a).replace('x', b)

        elif cmd == "reverse":
            a, b = int(args[1]), int(args[3])
            password = password[:a] + password[a:b+1][::-1] + password[b+1:]
        elif cmd == "move":
            a, b = (int(args[1]), int(args[4]))
            if reverse:
                a, b = b, a
            temp = password[:a] + password[a+1:]
            password = temp[:b] + password[a] + temp[b:]
        else:
            raise RuntimeError("Invalid input")

        if len(password) != orig_len:
            raise RuntimeError("Invalid input")

        if debug:
            print(f"  -> Result: {password}")
    return password


# print(exec("abcde", """swap position 4 with position 0
# swap letter d with letter b
# reverse positions 0 through 4
# rotate left 1
# move position 1 to position 4
# move position 3 to position 0
# rotate based on position of letter b
# rotate based on position of letter d""", debug=False))
#
#
# print(exec(password, s))

print(exec("fbgdceah", s, reverse=True, debug=True))
