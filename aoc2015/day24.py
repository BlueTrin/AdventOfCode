from aoc_lube import fetch
from math import prod
from more_itertools import set_partitions
import itertools

s = fetch(2015, 24)
pack_lst = [int(x) for x in s.splitlines() if x]

# bucket_size = sum(pack_lst) // 3
# print(f"bucket_size={bucket_size}")
#
# min_qe = 9999999999999
# for l in range(1, len(pack_lst)):
#     print(f"l={l}, min_eq={min_qe}")
#     for b1 in itertools.combinations(pack_lst, l):
#         if sum(b1) == bucket_size:
#             qe = prod(b1)
#             min_qe = min(min_qe, qe)
#
# print(f"part1: {min_qe}")

bucket_size = sum(pack_lst) // 4
print(f"bucket_size={bucket_size}")

min_qe = 9999999999999
for l in range(1, len(pack_lst)):
    print(f"l={l}, min_eq={min_qe}")
    for b1 in itertools.combinations(pack_lst, l):
        if sum(b1) == bucket_size:
            qe = prod(b1)
            min_qe = min(min_qe, qe)

print(f"part2: {min_qe}")