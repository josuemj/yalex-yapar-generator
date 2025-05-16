import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '...')))

from src.lexer import YALexLexer
from regex_afd.utils.visualizer import visualize_automaton

def main():
    yalex_file = "../examples/yalex/hard.yalex" # temp change
    input_file = "../examples/yalex/hard.txt" # temp change

    # Leer contenido del archivo de entrada correctamente
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
        print(token)


    # Mostrar errores si los hay
    if lexer.errors:
        print("\nErrores Léxicos Encontrados:")
        for error in lexer.errors:
            print(error)


if __name__ == "__main__":
    main()