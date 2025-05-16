class Item:
    def __init__(self, lhs, rhs, dot_position=0):
        self.lhs = lhs
        self.rhs = rhs
        self.dot = dot_position

    def next_symbol(self):
        if self.dot < len(self.rhs):
            return self.rhs[self.dot]
        return None

    def is_complete(self):
        return self.dot >= len(self.rhs)

    def advance(self):
        return Item(self.lhs, self.rhs, self.dot + 1)

    def __eq__(self, other):
        return (self.lhs, self.rhs, self.dot) == (other.lhs, other.rhs, other.dot)

    def __hash__(self):
        return hash((self.lhs, tuple(self.rhs), self.dot))

    def __str__(self):
        symbols = self.rhs[:]
        symbols.insert(self.dot, '~')
        return f"{self.lhs} -> {' '.join(symbols)}"