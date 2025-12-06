from aoc_lube import fetch
import math
from functools import cache
import numpy as np

def is_invalid_part1(idstr):
    return idstr[:(len(idstr)//2)] == idstr[(len(idstr)//2):]

def is_invalid_part2(idstr):
    for l in range(1, len(idstr)//2 + 1):
        patt = idstr[:l]
        if len([x for x in idstr.split(patt) if x != '']) == 0:
            return True
    return False

def main():
    invalid_ids_part1 = list()
    invalid_ids_part2 = list()
    s = fetch(2025, 2)

    # s = '''11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124'''
    for line in s.split(','):
        idmin, idmax = line.split('-')

        for idint in range(int(idmin), int(idmax)+1):
            idstr = str(idint)

            if is_invalid_part1(idstr):
                invalid_ids_part1.append(idint)

            if is_invalid_part2(idstr):
                invalid_ids_part2.append(idint)

    print(sum(invalid_ids_part1))
    print(sum(invalid_ids_part2))



if __name__ == "__main__":
    main()