from collections import defaultdict

def parse_yapar_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    # Separar secciones con %%
    parts = content.split('%%')
    if len(parts) != 2:
        raise ValueError("El archivo .yapar debe contener exactamente un separador '%%'.")

    # Extraer terminales
    header = parts[0]
    token_lines = [
        line.strip() for line in header.strip().splitlines()
        if line.strip().startswith('%token')
    ]

    terminales = set()
    for line in token_lines:
        line = line.replace('%token', '').strip()
        tokens = []
        i = 0
        while i < len(line):
            if line[i] == '"':
                i += 1
                start = i
                while i < len(line) and line[i] != '"':
                    i += 1
                tokens.append(line[start:i])
                i += 1  
            elif line[i].isspace():
                i += 1
            else:
                start = i
                while i < len(line) and not line[i].isspace():
                    i += 1
                tokens.append(line[start:i])
        terminales.update(tokens)

    # Extraer reglas de producción 
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
            grammar[lhs].extend(parse_productions(rhs))
        elif line.startswith('|'):
            rhs = line[1:].strip()
            grammar[current_lhs].extend(parse_productions(rhs))
        elif line.endswith(';'):
            continue
        else:
            raise ValueError(f"Línea no reconocida en el archivo .yapar: {line}")

    return {
        'terminales': terminales,
        'grammar': dict(grammar),
    }

def parse_productions(rhs):
    productions = []
    raw_prods = []
    current = ""
    in_quotes = False

    for c in rhs:
        if c == '"':
            in_quotes = not in_quotes
            current += c
        elif c == '|' and not in_quotes:
            raw_prods.append(current.strip())
            current = ""
        else:
            current += c
    if current:
        raw_prods.append(current.strip())

    for prod in raw_prods:
        prod = prod.rstrip(';').strip()
        if prod.lower() == 'epsilon' or prod == 'ε' or prod == '':
            productions.append(['ε'])
        else:
            symbols = []
            i = 0
            while i < len(prod):
                if prod[i] == '"':
                    i += 1
                    start = i
                    while i < len(prod) and prod[i] != '"':
                        i += 1
                    symbols.append(prod[start:i])
                    i += 1
                elif prod[i].isspace():
                    i += 1
                else:
                    start = i
                    while i < len(prod) and not prod[i].isspace():
                        i += 1
                    symbols.append(prod[start:i])
            productions.append(symbols)

    return productions
