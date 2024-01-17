import string
from functools import total_ordering
from typing import Iterable


@total_ordering
class Hand:

    def __init__(self, line: str or list, joker=False):
        if isinstance(line, str):
            cards, bid = line.split()
            self.bid = int(bid)
            self.cards = []
            for s in cards:
                match s:
                    case 'T':
                        c = 10
                    case 'J':
                        c = -1 if joker else 11
                    case 'Q':
                        c = 12
                    case 'K':
                        c = 13
                    case 'A':
                        c = 14
                    case _:
                        c = int(s)

                self.cards.append(c)
        else:
            self.cards = line[:]

        self._rank = self._compute_rank()

    def _compute_rank(self):
        buckets = {}
        for card in self.cards:
            if card not in buckets.keys():
                buckets[card] = len(list(filter(lambda c: c == card, self.cards)))

        buckets = tuple(sorted(list(buckets.values()), reverse=True))

        return {
            (5,): 6,
            (4, 1): 5,
            (3, 2): 4,
            (3, 1, 1): 3,
            (2, 2, 1): 2,
            (2, 1, 1, 1): 1,
            (1, 1, 1, 1, 1): 0
        }[buckets]

    def rank(self):
        return self._rank

    def __lt__(self, other):
        if self.rank() == other.rank():
            for card, other_card in zip(self.cards, other.cards):
                if card == other_card:
                    continue
                return card < other_card
        return self.rank() < other.rank()

    def __eq__(self, other):
        for card, other_card in zip(self.cards, other.cards):
            if card != other_card:
                return False

        return True


def read_lines(lines: Iterable[str]):
    return [Hand(line) for line in lines]
