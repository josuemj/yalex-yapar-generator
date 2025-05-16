import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.afn_afd import direct_method

def convert_to_regex(expr):
    """Convierte expresiones tipo ['a'-'Z'] o combinaciones a regex simple."""

    # Atajo para 'decimal'
    if expr == "digito+ punto digito*":
        return "[0-9]+\\.[0-9]*"  # Uno o más dígitos antes del punto, cero o más después
    
    expr = expr.replace('[', '').replace(']', '')
    expr = expr.replace("'", "")
    expr = expr.replace('"', '\\"')

    if expr.startswith('\\"') and expr.endswith('\\"'):
        return '".*?"'

    if len(expr) == 1:
        return expr

    if '-' in expr and len(expr) > 2:
        ranges = []
        i = 0
        while i < len(expr):
            if i + 2 < len(expr) and expr[i + 1] == '-':
                start_char = expr[i]
                end_char = expr[i + 2]
                if ord(start_char) > ord(end_char):
                    raise Exception(f"Rango inválido: {start_char}-{end_char}")
                ranges.extend([chr(c) for c in range(ord(start_char), ord(end_char) + 1)])
                i += 3
            else:
                ranges.append(expr[i])
                i += 1
        return f"[{''.join(ranges)}]"
    
    expr = expr.replace('+', '')  # Elimina "+" si no puedes procesarla
    expr = expr.replace('?', '')
    expr = expr.replace('*', '')

    return expr



def convert_to_dfa(expr):
    """Convierte la expresión regular a DFA"""
    dfa = direct_method(expr)
    return dfa
