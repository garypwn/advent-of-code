class BitmaskSet(type):
    """A metaclass for building bitmasks abstracted as sets. Given a collection of unique values, creates a class
    that can be used to store subsets of those values. Supports most set operations. Backed by a vector of bits
    signifying if an element is present or not.
    """

    class ClassFactory:
        _keymap: dict
        _max_len: int

        @classmethod
        def _try_cast(cls, item):
            try:
                return int(item)
            except TypeError:
                return int(cls(item))

        def __init__(self, *args):
            self.bits = 0
            if args:
                if len(args) > 1:
                    for val in args:
                        self.bits |= self._keymap[val]
                else:
                    if isinstance(args[0], int):
                        self.bits = args[0]
                    else:
                        for val in args[0]:
                            self.bits |= self._keymap[val]

        # Display operators
        def __repr__(self):
            return repr(set(self))

        def __str__(self):
            return repr(self)

        # BitmaskSet special operators
        def __int__(self):
            return self.bits

        @classmethod
        def _all(cls):
            return 2 ** cls._max_len - 1

        @classmethod
        def all(cls):
            """The set containing all possible elements in the set space. The universal set."""
            s = cls()
            s.bits = cls._all()
            return s

        def __invert__(self):
            """The absolute complement of the set."""
            s = type(self)()
            s.bits = self.bits ^ self._all()
            return s

        # Collections operators
        def add(self, val):
            self.bits |= self._keymap[val]

        def remove(self, val):
            self.bits &= self._all() ^ self._keymap[val]

        def __len__(self):
            return self.bits.bit_count()

        def __contains__(self, item):
            return self._keymap[item] & self.bits

        def __iter__(self):
            for k, b in self._keymap.items():
                if b & self.bits:
                    yield k

        # Set operators
        def __and__(self, other):
            s = type(self)()
            s.bits = self.bits & self._try_cast(other)
            return s

        def __or__(self, other):
            s = type(self)()
            s.bits = self.bits | self._try_cast(other)
            return s

        def __xor__(self, other):
            s = type(self)()
            s.bits = self.bits ^ self._try_cast(other)
            return s

        def __sub__(self, other):
            return self & ~self._try_cast(other)

        def __truediv__(self, item):
            """The set with a single element removed"""
            s = type(self)()
            s.bits = self.bits & (self._all() ^ self._keymap[item])
            return s

        # Comparison operators
        def __eq__(self, other):
            return self.bits == self._try_cast(other)

        def __hash__(self):
            return hash(self.bits)

        def __le__(self, other):
            return self & other == self

        def __lt__(self, other):
            return self != other and self <= other

        def __ge__(self, other):
            return self & other == other

        def __gt__(self, other):
            return self != other and self >= other

    def __new__(cls, keys, frozen=True):
        """
        Create a `BitMaskSet` type, returning a class that can be used to store subsets of the specified universal set.
        :param keys: The 'universe' of all possible elements that may be present in this set type
        :param frozen: If `True`, the type will be immutable, allowing hashing but disallowing addition and removal.
        """
        keys = keys if isinstance(keys, dict) else {k: 1 << i for i, k in enumerate(keys)}
        class_name = f"{'' if frozen else 'Mutable'}BitmaskSet_{len(keys)}"
        class_supers = ()

        class_attr = dict(BitmaskSet.ClassFactory.__dict__)
        class_attr['_keymap'] = keys
        class_attr['_max_len'] = len(keys.keys())
        class_attr['__doc__'] = cls.__doc__

        del class_attr['__dict__']
        del class_attr['__weakref__']

        if not frozen:
            del class_attr["remove"]
            del class_attr["add"]
            del class_attr["__hash__"]

        c = super().__new__(cls, class_name, class_supers, class_attr)

        return c


def test():
    c = BitmaskSet([1, 2, 3, 4, 5, 6])
    c1, c2 = c(1, 2, 3), c(3, 4, 5)
    print(c1 & c2)
    set()


test()
