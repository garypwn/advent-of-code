class Cycle:

    def __init__(self, offset, cyc):
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

    def accumulate(self, stop):
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
    def __init__(self, min_len=2):
        self._min_len = min_len
        self.values = []
        self.states = dict()
        self.cycle = None

    def send(self, item, state=None):
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

    def search_from_end(self):
        for i in range(self._min_len, len(self.values) + 1):
            if self.values[-i] == self.values[-1]:
                if self.values[-i + 1:] == self.values[-2 * i + 2:-i + 1]:
                    return Cycle(self.values[:-2 * i + 2], self.values[-i + 1:])
        return None
