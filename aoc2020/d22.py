from aoc_lube import fetch

s = fetch(2020, 22)

p1_s, p2_s = s.split('\n\n')
def read_deck(s):
    p1 = []
    p2 = []
    for r in p1_s.splitlines()[1:]:
        p1.append(int(r))

    for r in p2_s.splitlines()[1:]:
        p2.append(int(r))
    return p1, p2

#print(p1, p2)
p1, p2 = read_deck(s)
while p1 and p2:
    c1 = p1.pop(0)
    c2 = p2.pop(0)
    if c1 > c2:
        p1.extend([c1, c2])
    else:
        p2.extend([c2, c1])

score = sum((i + 1) * c for i, c in enumerate(reversed(p1 + p2)))
print(f"Part1: {score}")


def play_round(p1, p2):
    seen = set()
    while p1 and p2:
        if (tuple(p1), tuple(p2)) in seen:
            # Before either player deals a card, if there was a previous round in this game that had exactly the same
            # cards in the same order in the same players' decks, the game instantly ends in a win for player 1.
            return 1, p1
        seen.add((tuple(p1), tuple(p2)))
        c1 = p1.pop(0)
        c2 = p2.pop(0)
        if len(p1) >= c1 and len(p2) >= c2:
            # If both players have at least as many cards remaining in their deck as the value of the card they just
            # drew, the winner of the round is determined by playing a new game of Recursive Combat
            winner, _ = play_round(p1[:c1], p2[:c2])
        else:
            if c1 > c2:
                winner = 1
            elif c2 > c1:
                winner = 2
            else:
                raise RuntimeError("This should never happen")
        if winner == 1:
            p1.extend([c1, c2])
        elif winner == 2:
            p2.extend([c2, c1])
        else:
            raise RuntimeError("This should never happen")

    return (1, p1) if p1 else (2, p2)

p1, p2 = read_deck(s)
winner, deck = play_round(p1, p2)
score = sum((i + 1) * c for i, c in enumerate(reversed(deck)))
print(f"Part2: {score}")