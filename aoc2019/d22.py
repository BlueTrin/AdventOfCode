from aoc_lube import fetch
from functools import cache

s = fetch(2019, 22)

print(s)

def shuffle(deck, instructions):
    for instruction in instructions:
        if instruction.startswith('deal into new stack'):
            deck = deck[::-1]
        elif instruction.startswith('cut'):
            n = int(instruction.split()[-1])
            deck = deck[n:] + deck[:n]
        elif instruction.startswith('deal with increment'):
            n = int(instruction.split()[-1])
            new_deck = [0] * len(deck)
            for i, card in enumerate(deck):
                new_deck[(i * n) % len(deck)] = card
            deck = new_deck
    return deck

shuffled = shuffle(list(range(10007)), s.splitlines())
part1 = shuffled.index(2019)
print(f"Part1: {part1}")


def deal_into_new_stack(deck_size):
    return -1, -1

def cut_n_cards(n, deck_size):
    return 1, -n

def deal_with_increment_n(n, deck_size):
    return n, 0

def get_modular_factors(instructions, deck_size, times):
    a = 1
    b = 0
    for instruction in instructions:
        if instruction.startswith('deal into new stack'):
            f_a, f_b = deal_into_new_stack(deck_size)
        elif instruction.startswith('cut'):
            f_a, f_b = cut_n_cards(int(instruction.split()[-1]), deck_size)
        elif instruction.startswith('deal with increment'):
            f_a, f_b = deal_with_increment_n(int(instruction.split()[-1]), deck_size)
        else:
            raise ValueError(f"Unknown instruction: {instruction}")

        # f(g(x)) = a_f * ( a_g * x + b_g ) + b_f
        #         = a_f * a_g * x + a_f * b_g + b_f
        a = (f_a * a) % deck_size
        b = (f_a * b + f_b) % deck_size
    return a, b

deck_size = 119315717514047
times = 101741582076661

a, b = deal_into_new_stack(10)
assert (a * 0 + b)%10 == 9

a, b = cut_n_cards(3, 10)
assert (a * 0 + b)%10 == 7

a, b = deal_with_increment_n(3, 10)
assert a * 0 + b == 0
assert a * 1 + b == 3
assert (a * 7 + b) % 10 == 1

a, b = get_modular_factors('''deal with increment 7
deal into new stack
deal into new stack'''.splitlines(), 10, 1)
for pos, val in enumerate([0, 3, 6, 9, 2, 5, 8, 1, 4, 7]):
    assert (a * val + b) % 10 == pos

a, b = get_modular_factors('''cut 6
deal with increment 7
deal into new stack'''.splitlines(), 10, 1)
for pos, val in enumerate([3, 0, 7, 4, 1, 8, 5, 2, 9, 6]):
    assert (a * val + b) % 10 == pos

a, b = get_modular_factors('''deal with increment 7
deal with increment 9
cut -2'''.splitlines(), 10, 1)

for pos, val in enumerate([6, 3, 0, 7, 4, 1, 8, 5, 2, 9]):
    assert (a * val + b) % 10 == pos
pass
# test on part 1
a, b = get_modular_factors(s.splitlines(), 10007, 1)
pos_2019 = (a * 2019 + b) % 10007
assert pos_2019 == part1

