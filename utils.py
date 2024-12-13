import logging
import time
from typing import Dict, List, Tuple, Set

def aoc_timer(part=0, day=0, year=0):
    part = {1: 'one', 2: 'two'}.get(part)
    prepend = ''
    if year:
        prepend += '%s.' % year
    if day:
        prepend += '%s ' % day
    if part:
        prepend += 'part %s: ' % part
    def decorator(func):
        def wrapper(*a, **kw):
            try:
                start = time.perf_counter()
                result = func(*a, **kw)
                delta = (time.perf_counter() - start) * 1000
                if not prepend:
                    print(f'finished {func.__name__} in {delta:.4f} ms')
                else:
                    print(f'{prepend}{result} ({delta:.4f} ms)')
            except Exception as e:
                logging.exception(f'exception when solving {prepend}: {e}')
            else:
                return result
        return wrapper
    return decorator

def parse_space_separated(txt_input_str):
    '''
    >>> parse_space_separated("""1 2 3
    ... 4 5 6
    ... 7 8 9""")

    :param txt_input_str:
    :return:
    '''
    res = None
    for i_y, r in enumerate([r for r in txt_input_str.splitlines() if r]):
        for i_x, c in enumerate(r.split()):
            if res is None:
                res = [[] for i in  range(len(r.split()))]
            res[i_x].append(int(c))
    return res

def parse_complex(txt_input: str) -> Tuple[Dict[complex, str], Dict[str, Set[complex]], Tuple[int, int]]:
    '''
    Read input into complex coordinates
    >>> ex_txt_input = """.X.X
    ... ...
    ... .OO.
    ... """
    >>> ex_coords_to_char, ex_char_to_coordsset, ex_max_coords = parse_complex(ex_txt_input)

    :param txt_input:
    :return:
     (coords_to_char, char_to_coordsset, max_coords):
      -
    '''

    coords_to_char = {}
    char_to_coordsset = {}

    for i_y, r in enumerate(txt_input.split("\n")):
        if r:
            for i_x, c in enumerate(r):
                pt = i_x + i_y * 1j

                coords_to_char[pt] = c

                if c not in char_to_coordsset:
                    char_to_coordsset[c] = set()
                char_to_coordsset[c].add(pt)

    max_coords = (
        len(txt_input.split("\n")[0]),
        len([x for x in txt_input.split("\n") if x]))

    return coords_to_char, char_to_coordsset, max_coords

# if __name__ == '__main__':
#     from adventofcode.inputs import get_input
#     txt_input = get_input(8, year=2024)
#     coords_to_char, char_to_coordsset, max_coords = parse_complex(txt_input)
#     pass
