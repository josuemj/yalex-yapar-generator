def compute_first(grammar, terminals):
    first = {symbol: set() for symbol in grammar}
    for t in terminals:
        first[t] = {t}
    first['ε'] = {'ε'}

    changed = True
    while changed:
        changed = False
        for lhs, productions in grammar.items():
            for production in productions:
                i = 0
                while i < len(production):
                    symbol = production[i]
                    before = len(first[lhs])
                    first[lhs].update(first[symbol] - {'ε'})
                    if 'ε' in first[symbol]:
                        i += 1
                    else:
                        break
                else:
                    first[lhs].add('ε')
                if len(first[lhs]) > before:
                    changed = True
    return first
