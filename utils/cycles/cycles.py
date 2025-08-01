from collections.abc import Sequence


class Cycle[T]:
    """An infinite length sequence of values that contains a repeating pattern"""

    def __init__(self, offset: Sequence[T], cyc: Sequence[T]):
        """
        New infinite sequence with a repeating pattern
        :param offset: The initial non-cycling portion of the pattern
        :param cyc: The cycling portion of the pattern
        """
        self.cyc = cyc
        self._csum = sum(cyc)
        self.offset = offset
        self._off_sum = sum(offset)

    def __getitem__(self, item):
        if item < len(self.offset):
            return self.offset[item]
        return self.cyc[(item - len(self.offset)) % len(self.cyc)]

    def __iter__(self):
        for item in self.offset:
            yield item
        while True:
            for item in self.cyc:
                yield item

    def accumulate(self, stop: int) -> T:
        """
        Sum values in the cycle up to a given stopping point.
        :param stop: The stopping point
        :return: The sum of values in the range
        """
        if stop < len(self.offset):
            return sum(self.offset[:stop])

        result = self._off_sum
        rem = stop - len(self.offset)
        count, rem = divmod(rem, len(self.cyc))
        result += self._csum * count
        if rem > 0:
            result += sum(self.cyc[:rem])
        return result


class CycleFinder:
    """Finds a repeating pattern in a sequence of values"""

    def __init__(self, min_len=2):
        """
        New CycleFinder. Low min_length may result in false positives.
        :param min_len: The minimum length of cycle to consider.
        """
        self._min_len = min_len
        self.values = []
        self.states = dict()
        self.cycle = None

    def send(self, item, state=None):
        """
        Send a value and optional state to the cycle checker. Optionally, a state can be included to add context
        to the value.

        The cycle checker will check if there is a repeating sequence at the end of the sequence of inputted values.
        This check will occur each time a value is added (which may be slow.) If a state is included, it will instead
        only perform the check if the given state has occurred twice before.
        :param item: The value to search for patterns in.
        :param state: Hashable context such that if a given state appears twice it is guaranteed to be part of a cycle.
        :return: A Cycle object if a cycle is found, or else None.
        """
        cyc = self._check_cycle(state)
        self.values.append(item)
        return cyc

    def _check_cycle(self, state=None):

        if self.cycle:
            if not self.cycle[len(self.values) - 1] == self.values[-1]:
                self.cycle = None
                return None
            return self.cycle

        if state:
            if state in self.states:
                self.states[state] += 1
                if self.states[state] > 2:
                    return self.search_from_end()
            else:
                self.states[state] = 1
            return None

        else:
            if len(self.values) < 2 * self._min_len:
                return None

            self.cycle = self.search_from_end()
            return self.cycle

    def search_from_end(self) -> Cycle | None:
        """
        Check if there is a repeating sequence at the end of the sequence of values inputted into the CycleFinder.
        :return: A Cycle object if a cycle is found, or else None.
        """
        for i in range(self._min_len, len(self.values) + 1):
            if self.values[-i] == self.values[-1]:
                if self.values[-i + 1:] == self.values[-2 * i + 2:-i + 1]:
                    return Cycle(self.values[:-2 * i + 2], self.values[-i + 1:])
        return None
