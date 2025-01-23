from aoc_lube import fetch

s = fetch(2020, 8)
print(s)

acc = 0
ptr = 0
cmds = [((tokens:=r.split())[0], int(tokens[1])) for r in s.splitlines()]

def check_loop(cmds, ptr, acc, p2=False):
    seen = {}
    while ptr < len(cmds):
        if ptr in seen:
            return True, acc
        seen[ptr] = True
        op, arg = cmds[ptr]

        if op == 'acc':
            acc += arg
        elif op == 'jmp':
            if p2:
                is_loop, acc2 = check_loop(cmds, ptr+1, acc)
                if not is_loop:
                    return False, acc2, ptr
            ptr += arg
            continue
        elif op == 'nop':
            if p2:
                is_loop, acc2 = check_loop(cmds, ptr+arg, acc)
                if not is_loop:
                    return False, acc2, ptr
            pass

        ptr += 1
    return False, acc

_, acc = check_loop(cmds, ptr=0, acc=0)
print(f"Part1: {acc}")

is_loop, acc, ptrp2 = check_loop(cmds, ptr=0, acc=0, p2=True)
assert not is_loop
print(f"Part2: {acc}")