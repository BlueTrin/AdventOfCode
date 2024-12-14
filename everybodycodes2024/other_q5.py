import os, sys
import time


def main():
    with open(os.path.join(sys.path[0], "q5_p2.txt"), "r", encoding="utf-8") as f:
        text = f.read().strip()
        lines = text.split("\n")
    # transform chars into ints
    grid = [[int(x) for x in line.split()] for line in lines]
    # swap rows and columns
    grid = [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]

    # use a dict to keep track of the numbers we have seen
    seen_numbers: dict[str, int] = dict()
    # the row we are currently at
    current_row = 0
    # the round we are currently at
    round_counter = 1
    while True:
        # calculate the result of the current round
        result = calc_round(grid, current_row)
        # if we have seen the result 2024 times, print it and break
        if result in seen_numbers:
            seen_numbers[result] += 1
        else:
            seen_numbers[result] = 1
        if seen_numbers[result] == 2024:
            print(f"Round {round_counter}: {result}")
            print(round_counter * result)
            break
        # move to the next row
        current_row += 1
        if current_row >= len(grid):
            current_row = 0
        round_counter += 1


def calc_round(grid: list[list[int]], current_row: int):
    # the person we want to insert gets removed from the row
    person = grid[current_row].pop(0)
    # move to the next row
    current_row = current_row + 1
    # overflow to row 0
    if current_row >= len(grid):
        current_row = 0
    # the length of the row we will insert the person into
    row_len = len(grid[current_row])
    # how many steps are left over after traversing the row a single time
    left_over = person % row_len
    # how many times we traversed the row
    current_mod = person // row_len
    # if the steps are 0, the last traversal of the row is the one we want
    if left_over == 0:
        left_over = row_len
        current_mod -= 1
    # if we traversed the row an even amount (from front to back)
    if current_mod % 2 == 0:
        # insert person before
        grid[current_row].insert(left_over - 1, person)
    # if we traversed the row an odd amount (from back to front)
    else:
        # insert person after
        grid[current_row].insert(row_len - left_over + 1, person)
    return int("".join([str(x[0]) for x in grid]))


if __name__ == "__main__":
    before = time.perf_counter()
    main()
    print(f"Time: {time.perf_counter() - before:.6f}s")