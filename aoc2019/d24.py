import numpy as np
from scipy import signal
from aoc_lube import fetch
from collections.abc import Iterable

def func(val):
    if not isinstance(val, Iterable):
        return val
    return tuple(func(elem) for elem in val)

s = fetch(2019, 24)

# s = '''....#
# #..#.
# #..##
# ..#..
# #....'''
board = np.array([[int(c == '#') for c in line] for line in s.splitlines()])
print(board)

kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
#print(print(signal.convolve(board, kernel, mode='same')))

def next_status(s, neighbors):
    if s == 1:
        return int(neighbors == 1)
    return int(neighbors in (1, 2))

seen = set()
seen.add(func(board))

while True:
    new_board = np.array([[next_status(s, neighbors) for s, neighbors in zip(row, row_neighbors)]
                          for row, row_neighbors in zip(board, signal.convolve2d(board, kernel, mode='same'))])
    new_board_tuple = func(new_board)
    if new_board_tuple in seen:
        break
    else:
        seen.add(new_board_tuple)

    board = new_board

def biodiversity(board):
    return sum(2**i for i, s in enumerate(board.flatten()) if s)

print(f"Part1: {biodiversity(new_board)}")


# O M G NO MORE CONVOLVE for part2
board = np.array([[int(c == '#') for c in line] for line in s.splitlines()])
boards = {0: board}

def next_board(boards, level):
    if level not in boards:
        boards[level] = np.zeros((5, 5), dtype=int)
    board = boards[level]
    new_board = np.zeros((5, 5), dtype=int)
    for y in range(5):
        for x in range(5):
            if x == 2 and y == 2:
                continue
            neighbors = 0
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nx, ny = x+dx, y+dy
                if nx == 2 and ny == 2:
                    # neighbor is in the next level
                    if x == 1:
                        if level+1 in boards:
                            neighbors += boards[level+1][0, :].sum()
                    elif x == 3:
                        if level+1 in boards:
                            neighbors += boards[level+1][-1, :].sum()
                    elif y == 1:
                        if level+1 in boards:
                            neighbors += boards[level+1][:, 0].sum()
                    elif y == 3:
                        if level+1 in boards:
                            neighbors += boards[level+1][:, -1].sum()
                elif nx == -1:
                    # went on the left edge
                    if level-1 in boards:
                        neighbors += boards[level-1][1, 2]
                elif nx == 5:
                    # went on the right edge
                    if level-1 in boards:
                        neighbors += boards[level-1][3, 2]
                elif ny == -1:
                    # went on the top edge
                    if level-1 in boards:
                        neighbors += boards[level-1][2, 1]
                elif ny == 5:
                    # went on the bottom edge
                    if level-1 in boards:
                        neighbors += boards[level-1][2, 3]
                else:
                    neighbors += board[ny, nx]
            new_board[y, x] = next_status(board[y, x], neighbors)
    return new_board

t_max = 200

for t in range(t_max):
    new_boards = {}
    min_level = min(boards.keys())
    max_level = max(boards.keys())

    if boards[min_level].sum():
        boards[min_level-1] = np.zeros((5, 5), dtype=int)
    if boards[max_level].sum():
        boards[max_level+1] = np.zeros((5, 5), dtype=int)

    for level in range(min(boards.keys()), max(boards.keys())+1):
        new_boards[level] = next_board(boards, level)
    boards = new_boards

for level, board in boards.items():
    print(f"Depth {level}:")
    print(board)

    # input()

print(f"Part2: {sum(board.sum() for board in boards.values())}")
