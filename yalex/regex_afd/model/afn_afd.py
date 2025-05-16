def direct_method(expr):
    """Convierte regex a NFA y luego a DFA sin librerías."""
    # Construcción del NFA
    nfa = {}
    state_count = 0
    initial_state = state_count
    state_count += 1
    final_state = state_count
    state_count += 1

    if len(expr) == 1:
        # Literal de un solo carácter como '+', '*', '='
        nfa[(initial_state, expr)] = final_state
    elif expr.startswith('[') and expr.endswith(']'):
        # Manejar rango de caracteres como [a-zA-Z]
        char_range = expr[1:-1]
        for char in char_range:
            nfa[(initial_state, char)] = final_state
    else:
        # Expresión literal
        current_state = initial_state
        for char in expr:
            next_state = state_count
            nfa[(current_state, char)] = next_state
            current_state = next_state
            state_count += 1
        final_state = current_state
    
    # Conversión de NFA a DFA (algoritmo de subconjuntos)
    dfa = {}
    queue = [frozenset([0])]
    visited = set()

    while queue:
        current = queue.pop(0)
        visited.add(current)
        transitions = {}

        for state in current:
            for (src, char), dest in nfa.items():
                if src == state:
                    if char not in transitions:
                        transitions[char] = set()
                    transitions[char].add(dest)

        for char, dest_states in transitions.items():
            dest_frozen = frozenset(dest_states)
            if dest_frozen not in visited:
                queue.append(dest_frozen)
            dfa[(current, char)] = dest_frozen

    return dfa

