s = open("2015_07.txt").read()
s = s.replace(" AND ", " & ")
s = s.replace(" OR ", " | ")
s = s.replace(" RSHIFT ", " >> ")
s = s.replace(" LSHIFT ", " << ")
s = s.replace("NOT ", "65535 ^ ")
for k in ["is", "in", "as", "if", "id", "or"
          ]:
    s = s.replace(k, k+'_')
bigtext = s
del s

# override for part2
b = 16076
while True:
    for instruction in bigtext.splitlines():
        form, reg = instruction.split(" -> ")
        try:
            print(f"edec {reg} = {form}")
            if reg != "b":
                exec(f"{reg} = {form}")
            if reg == "a":
                print(f"a={a}")
                raise RuntimeError("found a")
        except NameError:
            print(f"skip {reg} = {form}")
            pass
        except Exception:
            print(f"err {reg} = {form}")
            raise

