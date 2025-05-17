from yapar.automaton.LR import Automaton

def extract_symbols(grammar_dict, token_set):
    all_rhs_symbols = set()
    for prods in grammar_dict.values():
        for prod in prods:
            all_rhs_symbols.update(prod)

    non_terminals = set(grammar_dict.keys())
    terminals = (all_rhs_symbols - non_terminals)

    # Filtrar para dejar solo los que están en los terminales
    terminals = terminals.intersection(token_set)

    return terminals, non_terminals

def build_from_grammar(parsed_result):
    grammar = parsed_result['grammar']
    terminales = parsed_result['terminales']
    start_symbol = next(iter(grammar))  # primer símbolo no terminal

    # Agregar producción inicial aumentada
    augmented_start = f"{start_symbol}'"
    grammar[augmented_start] = [[start_symbol]]

    terminals, non_terminals = extract_symbols(grammar, terminales)

    automaton = Automaton(grammar, terminals, non_terminals, start_symbol)
    return automaton