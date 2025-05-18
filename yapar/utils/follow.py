def compute_follow(grammar, terminals, first, start_symbol):
    follow = {non_terminal: set() for non_terminal in grammar}
    follow[start_symbol].add('$')  # Símbolo de fin de cadena

    changed = True
    while changed:
        changed = False
        for lhs, productions in grammar.items():
            for production in productions:
                trailer = follow[lhs].copy()
                for symbol in reversed(production):
                    if symbol in grammar:  # es no terminal
                        before = len(follow[symbol])
                        follow[symbol].update(trailer)
                        if 'ε' in first[symbol]:
                            trailer.update(first[symbol] - {'ε'})
                        else:
                            trailer = first[symbol]
                        if len(follow[symbol]) > before:
                            changed = True
                    else:
                        trailer = first[symbol]
    return follow
