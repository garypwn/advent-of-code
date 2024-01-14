# Scratchcards are two lists of ints (winning numbers), (my numbers)
from typing import Iterable


def read_lines(lines: Iterable[str]):
    cards = []
    for line in lines:
        cards.append(scratch_card(line))

    return cards


def scratch_card(line: str):
    parts = line.split('|')
    parts[0] = parts[0].split(':')[1]
    winners, nums = [[int(i) for i in part.split()] for part in parts]
    return set(winners), set(nums)


def matches(winners, numbers):
    return len(winners & numbers)


def points(winners, numbers):
    m = matches(winners, numbers)
    return 2 ** (m - 1) if m >= 1 else 0


def play(cards):
    # Play until we run out of cards

    count = 0
    winners = [matches(*card) for card in cards]

    active = [1 for _ in cards]
    remaining = len(active)

    while remaining > 0:
        remaining = 0
        next_round = [0 for _ in cards]
        for i, n in enumerate(active[:]):

            count += n
            for j in range(i+1, i+1+winners[i]):
                next_round[j] += n
                remaining += n

        active = next_round

    return count


