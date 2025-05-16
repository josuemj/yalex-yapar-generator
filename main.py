from utils.parser_utils import parse_yapar_file
from yapar.build_automaton import build_from_grammar

parsed = parse_yapar_file('./examples/yapar/easy.yalp')

print("Terminales:", parsed['terminales'])
print("Grammar:")
for lhs, prods in parsed['grammar'].items():
    for prod in prods:
        print(f"{lhs} -> {' '.join(prod)}")

print("\n===============AUTOMATON=======================\n")
automaton = build_from_grammar(parsed)
print(automaton)