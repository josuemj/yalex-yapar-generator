from collections import defaultdict

def build_slr_table(automaton, grammar, terminals, follow, augmented_start):
    ACTION = defaultdict(dict)
    GOTO = defaultdict(dict)

    # Todas las producciones (para reducir)
    productions = []
    for lhs, prods in grammar.items():
        for prod in prods:
            productions.append((lhs, prod))

    for state_id, state in enumerate(automaton.states):
        for item in state:  # ✅ state es un set de Item
            lhs, rhs, dot_pos = item.lhs, item.rhs, item.dot

            # 1. ACCEPT
            if lhs == f"{augmented_start}'" and dot_pos == len(rhs):
                ACTION[state_id]['$'] = ('accept',)

            # 2. REDUCE
            elif dot_pos == len(rhs):  # punto al final
                for terminal in follow[lhs]:
                    ACTION[state_id][terminal] = ('reduce', lhs, rhs)

            # 3. SHIFT o GOTO
            else:
                symbol_after_dot = rhs[dot_pos]
                next_state = automaton.transitions.get((state_id, symbol_after_dot))
                if next_state is not None:
                    if symbol_after_dot in terminals:
                        ACTION[state_id][symbol_after_dot] = ('shift', next_state)
                    else:
                        GOTO[state_id][symbol_after_dot] = next_state

    return ACTION, GOTO
