
# from adventofcode.inputs import get_input
# from adventofcode.utils import aoc_timer
import logging
import math
from heapq import heappop, heappush

logging.basicConfig()

logger = logging.getLogger(__name__)

N = -1j
S = 1j
E = 1
W = -1

CONV_MAP = {
    "^": N,
    "v": S,
    "<": W,
    ">": E,
}

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

INV_CONV_MAP = {v: k for k, v in CONV_MAP.items()}

def parse_input(i):
    lines = i.split("\n")
    x_entrance = lines[0].find(".") - 1
    x_exit = lines[-1].find(".") - 1
    bliz_lst = []
    for i_y, l in enumerate(lines[1:-1]):
        for i_x, c in enumerate(l[1:-1]):
            if c != ".":
                bliz_lst.append((i_x+ i_y*1j, CONV_MAP[c]))
        if logger.level <= logging.DEBUG:
            logger.debug(f"after `{l}` found `{len(bliz_lst)}' blizz")

    map_size = len(lines[-1])-3 + (len(lines)-3)* 1j

    return (x_entrance - 1j), x_exit + (map_size.imag+1) * 1j, map_size, bliz_lst

def forward_blizzard(map_size, blizz_lst, turn):
    res = []
    for blizz in blizz_lst:
        blizz_cooord = blizz[0] + blizz[1] * turn
        blizz_cooord_x = blizz_cooord.real % (map_size.real+1)
        blizz_cooord_y = blizz_cooord.imag % (map_size.imag+1)
        blizz_cooord = blizz_cooord_x + blizz_cooord_y * 1j
        res.append((blizz_cooord, blizz[1]))
    return res

# def safe_position(coords_set, map_size, blizz_lst, turn):
#     '''
#     Modify in place coord_lst with the coordinates that are not in the blizz
#     :param coord_lst:
#     :param map_size:
#     :param blizz_lst:
#     :param turn:
#     :return:
#     '''
#     fwd_blizz_lst = forward_blizzard(map_size, blizz_lst, turn)
#     for blizz_cooord, _ in fwd_blizz_lst:
#         for coord in enumerate(coords_set):
#             if coord == blizz_cooord:
#                 coord_lst[i_coord] = None
#     return [coord for coord in coord_lst if coord is not None]

def expand_coord(coords_set, map_size, blizz_set, exit_coord):
    res = set()
    for coord in coords_set:
        if coord not in blizz_set:
            res.add(coord)   # allows to stay in place
        for d in [N, S, W, E]:
            next_coord = coord + d
            if next_coord == exit_coord:
                res.add(next_coord)
            elif 0 <= next_coord.real <= map_size.real and 0 <= next_coord.imag <= map_size.imag and next_coord not in blizz_set:
                res.add(next_coord)
    return res

def solve_puzzle(start_coord, exit_coord, map_size, blizz_lst, turn = 0):
    coords_set = {start_coord}

    if logger.level <= logging.DEBUG:
        print_state(coords_set, start_coord, exit_coord, map_size, blizz_lst, turn)
    while True:
        turn += 1

        fwd_blizz_lst = forward_blizzard(map_size, blizz_lst, turn)
        fwd_blizz_set = {x[0] for x in fwd_blizz_lst}
        potential_coords = expand_coord(coords_set, map_size, fwd_blizz_set, exit_coord)
        # potential_coords = safe_position(potential_coords, map_size, blizz_lst, turn)

        if len(potential_coords) == 0:
            raise RuntimeError("Failed to find a solution")

        if logger.level <= logging.DEBUG:
            print_state(potential_coords, start_coord, exit_coord, map_size, blizz_lst, turn)

        if exit_coord in potential_coords:
            return turn

        coords_set = potential_coords

def print_state(coords, start_coord, exit_coord, map_size, blizz_lst, turn):
    '''
    Debug function to print the grid
    :param coords:
    :param start_x:
    :param exit_x:
    :param nmap_size:
    :param blizz_lst:
    :return:
    '''

    res_lst = []
    first_row = '#'  * (int(map_size.real) + 3)
    if start_coord.imag == -1:
        first_row = first_row[:int(start_coord.real)+1] + 'E' + first_row[int(start_coord.real)+2:]
    else:
        first_row = first_row[:int(exit_coord.real)+1] + '.' + first_row[int(exit_coord.real)+2:]
        # raise RuntimeError("should not happen")
    res_lst.append(first_row)

    updated_blizz_lst = forward_blizzard(map_size, blizz_lst, turn)
    for i_y in range(int(map_size.imag)+1):
        row = '#'
        for i_x in range(int(map_size.real)+1):

            blizz_at_coords = [blizz for blizz in updated_blizz_lst if blizz[0] == (i_x + i_y * 1j )]

            if len(blizz_at_coords) > 1:
                row += f'{len(blizz_at_coords)}'
            elif len(blizz_at_coords) == 1:
                row += f'{INV_CONV_MAP[blizz_at_coords[0][1]]}'
            elif (i_x + i_y * 1j ) in coords:
                row += 'E'
            else:
                row += '.'
        row += '#'
        res_lst.append(row)

    last_row = '#'  * (int(map_size.real) + 3)
    if start_coord.imag == map_size.imag + 1:
        last_row = last_row[:int(start_coord.real)+1] + '.' + last_row[int(start_coord.real)+2:]
    else:
        last_row = last_row[:int(exit_coord.real) + 1] + '.' + last_row[int(exit_coord.real) + 2:]
    res_lst.append(last_row)

    logger.debug(f'turn={turn}\n'+'\n'.join(res_lst))


if __name__ == '__main__':
    # logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)

#     example = '''#.#####
# #.....#
# #>....#
# #.....#
# #...v.#
# #.....#
# #####.#'''
#     i = parse_input(example)
#     t = solve_puzzle(*i)
#     print(t)


    example = '''#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#'''
    i = parse_input(example)
    t = solve_puzzle(*i)
    print(t)


    part1 = '''#.####################################################################################################
#<<^<<v.v^>v.<v>.^^>vvv<..^><>vvv>v>.v<>^>vv<<^><<^.<v^^<<<<<v^v><v>v^>vv>>.<^>.>^^^.<><><^^<v^><><.<#
#<<^<<vv^vv<<^<><>>^<^vvv><>>>^.<v^<..<.>v>v>vvv><.v<^>v^v<<<>>>>>vv<^<<<v>^<.>>vv><<.>v<.^v.v<^<>>v>#
#<<.v>.v<v<<^v.v>><v.<v<^.>>>.<^>^^^><<>.v><<vv.^v^.^<v>v^vv^<.>v<v><.v^.v<v<v>>><^v.v^^^<<v<^^<>v>v>#
#<>^v>vvv><..^..v<<^v^><.<<<<>>>^v><.<<^^vv<^v.<^^<^v^>>vv<.>v><..^><.vv>v^>>v><^v<<<^v<^v<v<<^v.vv^>#
#>^v<>>v<^^vv<<<v^v^<<v>v^vv^vv>><>^.^vv^<>^<v^^<.^v<.^<>^>vv.><<^>v<^^>v^<v.^.^<>v>^>v.<^vvvv<>>.>v>#
#<^^>><v><<^v<v>vvv>v^>v<^^^^><>^v^.<v^>.<>>vvv^v>.<v<<<^v>>>><v^^<>^v<>>^v>^^^^vvv^^><>^^^^<v<..><^>#
#>><<<><>^v^<<v>>.<v^^^^<vv^>>>v<v><v>>^>>^^^>v.<v^v>><><^v><vv<^.^vvvv<>.^>v><<<^>vv<^^v<v^^<><.^^v.#
#<>>^^>v<v.>v.v>^<<>^.>>vv^vv<^>v^><.^v<<v^<.^>v^.^v.<^.^<^<..^>><>v.>^v>vvvv<<>v^<vv<>vv>v>.>v^<^^^>#
#>vv<v>v<v>^<>v^<^vv<>v>^><><<>>v^<>v.<.>>>>v<v>v^<v<^v<>>v^<>v^>v>v<^<^v^^<v.<^vv<<<.>^v^><v>^^<.<>>#
#>v^.>vv^vv>.><<^.v^.v<>.^>v><<>v^^<<^<.^.^vv^<^^^><<>.v<<v<v<^^>v<<^<vv^^>>vvv>vvv<^vv.^.v>.<v.><^v>#
#<><>^v^^<.vv<v>^v<<^v>^.<v>^<.>.>^.v<<^vv.vv<v^<v<^v.>^^^<^^><^vv<<<>v<>><vv.<.<<vv<v.<<.>^>>>^>^.^>#
#<^><v<><v>v^^<^<vv>^^>^v^>v^>^>><v.>^<.<v<>.<^>>^<<^v^v^.><>v><<^^^vvv<><^>^^v.>><>>v<<^.v<v>^<>v^<<#
#>.><<<^<v<v>vv>v><.<v>.^^<<<<<><v>^.><^>vvv>v^<^<^v^<><>>.<v<v^v><^.vv^^>^vv>v^<v^<<<>^.v^<vv<v^v>.>#
#>.<>^><v><.^>vv.^.>v<<v^<^<><>...<>.>^<^><<>v>^>^<.^><><v<>v>>.<^v^<.<vv^v>.v^<v>vv>v>>>^.<^<v^<<..<#
#>^<<><<^>vvv>>>>v<<^v^>><>..^>v>>^<v>>v^^^.>.<>.^<^<v^>>v><.v>^v<v>v<^.^<^v<.v>^v>v>^>>^^v>>>>^^^^<<#
#>><^^v>vv>v<^<><v>vv^>^^^v^<^<><.<<^^>><<>v><><<>^<^>v^v^v<><v.><v>>..v^><v>><v^<^vvv>v.^^<<><>v.<><#
#>^^vv<<>>^^^>v<<<<v>.v^>v>v>vvv<^^<<v<.^^<<^^v<<><<>v.vv.^>^>><^><<vv>^.<>>v>^^v>^vv>.^^v>^.vvv>><<<#
#><^^^>vv.<^>^<><vv<><^^v<v.>.vv><^<.^^.v<vv<v<<<^<vvv.^^v^>^v.>^v<<<^vv><<v..^<v<^>>.^^^>v<><^vv^<v<#
#<>^^.>><v>v>^^.v<>.^vv^>.<^<vv<<v<v<v>.<^v>.<><v><^<^^>v>>^>.^>>^><.<><^<<v^v^<>vv<<<>>>^>^<vv^v<^^<#
#<>v^v><<v<v<.v><vv^v>><>><^.>>^vv>^.<v^^<^><>v<v^<v>vv>^v>vv<<v^>>>^>>>><>vvvv<^>v>^^>>^>^^^..^<v^<>#
#>v^<^^>v^v^<^>.<vv.<^>>>v.v^^<<^^<.<^.v<<^>v.>^v<.vvv^<vv<><>.v^>>vv<<<v>vvv>^<>^<vvv><v^vv<^^v>^<^<#
#<v^^v><.>>vv^.>>>^^><.v><<>^^><vv<><>v^v<<v^<v><.vv><<>>^^^>vvvv.^<<>vv.<.v.v<><><>.<><^^>v>v>v.^^<<#
#<>v^^<v^^>^>^<<<><<<^^>v>^><^v^>.<^^.<<.<v>><..^<v^^><^<<<.<.vvv.<<^v^<<<>v^.<^><>>.^>v<>^v><.^^>^><#
#><<^^^vvv^^>v^v^>v<v.v^<<<v^><>v><<vvv.v<>vv<<^^^><v^vv.>^<^><^>>v>.^<^^v^<<^><<^.^>vvv>>>.<><^v^^<<#
#<>>vv.^^^<^^>v<<>^>>v^<v.vv<vv^.<<v><v>v^>>>^^<.><^v^vvv..><><>v.^.v<vv><>v>><><>v^<<^.^^^v<^>>^<^^>#
#<>>.^>>v<>>>^<v>.>^><>^^>^vv>vv^><.<<<<<^<>.^.v^vv><v<vv>vv^^<><^.^>>v^<><><^v<v.>^^^>^v^^<v^><^<..>#
#><..>vv<<>vv^vv^>>.^^>^v><^^v<<..<^>.>^<vv^v>>><v^.>v^<>..<^<<<^>v^v<>v><vvv^^v^<>vv^<<<v<<vv<>>v^v>#
#>v<^>v<>v.v<>^vv.^<>v>>^v>.^^^>^<v^^>v>^><..v>v.>vvv^.^<v><^^v.^^<^vv..v^^^.>><>vvv>^vv^v<>>v^>v^v^.#
#>v><<^<.<^<<v.^^v^^^>>vv<^<^^.^^^v.<<.^>^>.<vv<v<^.>.^v^^v<><><^<^<^>v<><>^^<<<<>^..>v>><>^.v^.<>^^>#
#>>^^^^^v.<<>^^v>^vv.^<.<v^.^.^^>v<^^v<>v<^.>v<<<^>v^vv^><>>^^.><<>.v<^v^<>>^<>^v>v>>^^.<v<>v>.>vv^<.#
#<<^v>^^>^>.<^<>vvv^^v>v<<>v<.><^<<v><v<.v>v^>>>^v<vv>>>>>v^>.^^^>^.<<>vv<^v<>v>v^vv>v><.v.>.v><><.><#
#>v.^>v^^<>>v^.>^<<>><vv><<v<^>^<>.^<>>^^>^^>.><^>vv<<<v><^<<vv>^.^<v<<>v^.<<<.<>^<^v<^^<^>v>><.^>.<<#
#><<<<.^.vvvv^^<v^^^...<>v<<<v^^<v<.>>>><<^^<>^vv<<<v^^><.<^><<.<>vv<><>vv^>>vvv^^.><^<<v>^^^^.<v>>>>#
#<^.>>^vv<v<<v>>^>v.>^.vv^.>^<^v^.^<..><<.vvv>>vv>.^v^.>^<vv^vv^<^>>^>^>><<<^vv.^.>^>><v>v^v><^<>vv^>#
#..v^>..>v....v<vv^<^.^>v.<.>^<<vv^^^>v^<<>v^v^>^<<>v^^^>.<^>^<<.v.v<<<^>>><^<^<<>.^^^<<<><^^^vv<vv.<#
####################################################################################################.#'''
    start_coord, exit_coord, map_size, blizz_lst = parse_input(part1)
    t1 = solve_puzzle(start_coord, exit_coord, map_size, blizz_lst)
    print(t1)

    t2 = solve_puzzle(exit_coord, start_coord, map_size, blizz_lst, turn=t1)
    print(t2)

    t3 = solve_puzzle(start_coord, exit_coord, map_size, blizz_lst, turn=t2)
    print(t3)
