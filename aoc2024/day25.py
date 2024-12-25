lock_l, key_l = [], []
for schem in open("2024_25.txt").read().split("\n\n"):
    cols = [s.count("#") for s in list(zip(*schem.splitlines()))]
    lock_l.append(cols) if schem[0] == '#' else key_l.append(cols)
print(sum([all(lo+k < 7 for lo, k in zip(lock, key)) for lock in lock_l for key in key_l]))

# one liner
import itertools, more_itertools
print(sum([all(lo+k < 7 for lo, k in zip(lock, key)) for (_, lock), (_, key) in itertools.product(*more_itertools.partition(lambda v: v[0] == '#',[(schem[0],[s.count("#") for s in list(zip(*schem.splitlines()))]) for schem in open("2024_25.txt").read().split("\n\n")]))]))
