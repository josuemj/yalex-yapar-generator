from collections import defaultdict
from .token_map import TOKEN_MAP
from .item import Item

def cerradura(items, grammar):
    closure_set = set(items)
    added = True

    while added:
        added = False
        new_items = set()

        for item in closure_set:
            symbol = item.next_symbol()
            if symbol and symbol in grammar:
                for production in grammar[symbol]:
                    new_item = Item(symbol, production)
                    if new_item not in closure_set:
                        new_items.add(new_item)

        if new_items:
            closure_set |= new_items
            added = True

    return closure_set

def ir_A(items, symbol, grammar):
    goto_items = {item.advance() for item in items if item.next_symbol() == symbol}
    return cerradura(goto_items, grammar)

class Automaton:
    def __init__(self, grammar, terminals, non_terminals, start_symbol):
        self.grammar = grammar
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.start_symbol = start_symbol
        self.states = []
        self.transitions = {}
        self.build()

    def build(self):
        augmented_start = Item(f"{self.start_symbol}'", [self.start_symbol])
        start_state = cerradura([augmented_start], self.grammar)
        self.states.append(start_state)
        pending = [start_state]
        seen = {frozenset(start_state): 0}

        while pending:
            state = pending.pop()
            state_index = self.states.index(state)
            symbols = self.terminals | self.non_terminals

            for symbol in symbols:
                new_state = ir_A(state, symbol, self.grammar)
                if not new_state:
                    continue
                key = frozenset(new_state)
                if key not in seen:
                    seen[key] = len(self.states)
                    self.states.append(new_state)
                    pending.append(new_state)
                self.transitions[(state_index, symbol)] = seen[key]

    def __str__(self):
        result = ""
        for idx, state in enumerate(self.states):
            result += f"State {idx}:\n"
            for item in state:
                result += f"  {item}\n"

        result += "\nTransitions:\n"
        for (src, sym), dst in self.transitions.items():
            sym_repr = TOKEN_MAP.get(sym, sym)
            result += f"  State {src} --[{sym_repr}]--> State {dst}\n"
        return result