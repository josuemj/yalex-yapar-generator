import re
from collections import defaultdict

def parse_yapar_file(filepath):
    with open(filepath, 'r') as file:
        content = file.read()

    # Separar secciones
    parts = content.split('%%')
    if len(parts) != 2:
        raise ValueError("El archivo .yapar debe contener exactamente un separador '%%'.")

    # 1. Extraer terminales
    header = parts[0]
    token_lines = [line.strip() for line in header.strip().splitlines() if line.strip().startswith('%token')]
    terminales = set()
    for line in token_lines:
        terminales.update(line.replace('%token', '').strip().split())

    # 2. Extraer reglas de producción
    grammar_text = parts[1].strip()
    lines = [line.strip() for line in grammar_text.splitlines() if line]

    grammar = defaultdict(list)
    current_lhs = None

    for line in lines:
        if ':' in line:
            lhs, rhs = line.split(':', 1)
            lhs = lhs.strip()
            rhs = rhs.strip()
            current_lhs = lhs
            productions = [p.strip().rstrip(';').split() for p in rhs.split('|')]
            grammar[lhs].extend(productions)
        elif line.startswith('|'):
            rhs = line[1:].strip()
            productions = [p.strip().rstrip(';').split() for p in rhs.split('|')]
            grammar[current_lhs].extend(productions)
        elif line.endswith(';'):
            continue
        else:
            raise ValueError(f"Línea no reconocida en el archivo .yapar: {line}")

    return {
        'terminales': terminales,
        'grammar': dict(grammar),
    }