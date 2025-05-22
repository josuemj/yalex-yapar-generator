from utils.parser_utils import parse_yapar_file
from yapar.build_automaton import build_from_grammar
from yapar.visualizer import render_automaton
from yapar.utils.parse_driver import parse_tokens, resolve_token_symbol

#yalex stuff
from yalex.src.lexer import YALexLexer

#fist follow
from yapar.utils.first import compute_first
from yapar.utils.follow import compute_follow

#table
from yapar.utils.build_slr_table import build_slr_table


parsed = parse_yapar_file('./examples/yapar/easy.yalp')

# NOTE: Move to test
#EJEMPLO EN CLASE  
# grammar = {
#     'E': [['E', '+', 'T'], ['T']],
#     'T': [['T', '*', 'F'], ['F']],
#     'F': [['(', 'E', ')'], ['id']]
# }

# terminales = {'+', '*', '(', ')', 'id'}

# parsed = {
#     'terminales': terminales,
#     'grammar': grammar
# }

print("Terminales:", parsed['terminales'])
print("Grammar:")
for lhs, prods in parsed['grammar'].items():
    for prod in prods:
        print(f"{lhs} -> {' '.join(prod)}")
        
print("\n===============FIRST FOLLLOW=======================\n")
        
grammar = parsed['grammar']
terminals = parsed['terminales']
start_symbol = 'Program' #list(grammar.keys())[0] 
for lhs, prods in grammar.items():
    for prod in prods:
        if 'epsilon' in prod:
            print(f"❌ ¡Error! Producción contiene 'epsilon' literal: {lhs} -> {prod}")
            
first = compute_first(grammar, terminals)
follow = compute_follow(grammar, terminals, first, start_symbol)

print("\n==== FIRST ====")
for nt, f in first.items():
    if nt in grammar:  # Solo no terminales
        print(f"FIRST({nt}) = {f}")

print("\n==== FOLLOW ====")
for nt, f in follow.items():
    print(f"FOLLOW({nt}) = {f}")

print("\n===============AUTOMATON=======================\n")
automaton = build_from_grammar(parsed)
print(automaton)


automaton = build_from_grammar(parsed)
render_automaton(automaton, output_path='output/automaton', format='png')
print("\n===============Se ha creado el automata en PNG=======================\n")

augmented_start = start_symbol  
ACTION, GOTO = build_slr_table(automaton, grammar, terminals, follow, augmented_start)

print("\n==== TABLA ACTION ====")
for state, actions in ACTION.items():
    for symbol, action in actions.items():
        print(f"ACTION[{state}, {symbol}] = {action}")

print("\n==== TABLA GOTO ====")
for state, transitions in GOTO.items():
    for symbol, next_state in transitions.items():
        print(f"GOTO[{state}, {symbol}] = {next_state}")

print("\n===============VERIFICACIÓN DE CADENA=======================\n")

# NOTE: Move to test
# Cadena: id + id * id → simula tokens (como saldrían del lexer)
# tokens = [
#     ('id', 'x'),
#     ('+', '+'),
#     ('id', 'y'),
#     ('*', '*'),
#     ('id', 'z'),
# ]

# Verificar con el parser SLR

        
### FLUJO YALEX - YAPAR

difficulty = "easy" # "easy", "complex"

yalex_file = f"examples/yalex/{difficulty}.yalex" # temp change
input_file = f"examples/input_strings/{difficulty}.txt" # temp change

with open(input_file, 'r', encoding='utf-8') as f:
  input_text = f.read()

print("Texto a ver: ", input_text)

# Crear analizador léxico
lexer = YALexLexer(yalex_file)
lexer.build_dfa()
#visualize_automaton(lexer)


# Procesar entrada  
lexer.tokenize(input_text)  # Add debug parameter if supported

# Mostrar los tokens generados
print("\nTABLA DE TOKENS")
for token in lexer.tokens:
    print("\n=============== PARSEANDO CON YAPar ===============\n")
    print(token)
    tokens = [(resolve_token_symbol(t), t['value']) for t in lexer.tokens]

    success = parse_tokens(tokens, ACTION, GOTO, start_symbol)

    if success:
        print(" Cadena aceptada por el parser.")
    else:
        print(" Cadena rechazada por el parser.")

# Mostrar errores (lexicos) si los hay
if lexer.errors:
  print("\nErrores Léxicos Encontrados:")
  for error in lexer.errors:
      print(error)