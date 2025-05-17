from utils.parser_utils import parse_yapar_file
from yapar.build_automaton import build_from_grammar
from yapar.visualizer import render_automaton

#yalex stuff
from yalex.src.lexer import YALexLexer

#parsed = parse_yapar_file('./examples/yapar/hard.yalp')

grammar = {
    'E': [['E', '+', 'T'], ['T']],
    'T': [['T', '*', 'F'], ['F']],
    'F': [['(', 'E', ')'], ['id']]
}

terminales = {'+', '*', '(', ')', 'id'}

parsed = {
    'terminales': terminales,
    'grammar': grammar
}

print("Terminales:", parsed['terminales'])
print("Grammar:")
for lhs, prods in parsed['grammar'].items():
    for prod in prods:
        print(f"{lhs} -> {' '.join(prod)}")

print("\n===============AUTOMATON=======================\n")
automaton = build_from_grammar(parsed)
print(automaton)


automaton = build_from_grammar(parsed)
render_automaton(automaton, output_path='output/automaton', format='png')
print("\n===============Se ha creado el automata en PNG=======================\n")

### TEST DEL YALEX
#
#difficulty = "complex" # "easy", "complex"
#
#yalex_file = f"examples/yalex/{difficulty}.yalex" # temp change
#input_file = f"examples/input_strings/{difficulty}.txt" # temp change
#
#with open(input_file, 'r', encoding='utf-8') as f:
#    input_text = f.read()
#
#print("Texto a ver: ", input_text)
#
## Crear analizador léxico
#lexer = YALexLexer(yalex_file)
#lexer.build_dfa()
##visualize_automaton(lexer)
#
#
## Procesar entrada  
#lexer.tokenize(input_text)  # Add debug parameter if supported
#
## Mostrar los tokens generados
#print("\nTABLA DE TOKENS")
#for token in lexer.tokens:
#    
#    # aca iria la interaccion con el Yapar :)
#    
#    print(token)
#
## Mostrar errores si los hay
#if lexer.errors:
#    print("\nErrores Léxicos Encontrados:")
#    for error in lexer.errors:
#        print(error)
#
