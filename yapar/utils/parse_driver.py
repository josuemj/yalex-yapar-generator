def parse_tokens(tokens, action_table, goto_table, count, start_symbol):
    stack = [0]
    index = 0
    logs = []
    a = tokens[index][0] if tokens else '$'

    while True:
        s = stack[-1]
        action = action_table.get(s, {}).get(a)

        if action is None:
            value = tokens[index][1] if index < len(tokens) else 'EOF'
            print(f"Error sintáctico en línea {count}: no hay acción definida para estado {s} y símbolo '{a}' (valor: '{value}')")
            logs.append(f"Error sintáctico en línea {count}: no hay acción definida para estado {s} y símbolo '{a}' (valor: '{value}')")
            return False, logs

        if action[0] == 'shift':
            t = action[1]
            print(f"Shift: símbolo '{a}' → estado {t}")
            logs.append(f"Shift: símbolo '{a}' → estado {t}")
            stack.append(t)
            index += 1
            a = tokens[index][0] if index < len(tokens) else '$'

        elif action[0] == 'reduce':
            A, beta = action[1], action[2]
            for _ in beta:
                stack.pop()
            t = stack[-1]
            goto_state = goto_table.get(t, {}).get(A)
            if goto_state is None:
                print(f"Error en línea {count}: acción inválida en estado {s} con símbolo '{a}'")
                logs.append(f"Error en línea {count}: acción inválida en estado {s} con símbolo '{a}'")
                return False, logs
            stack.append(goto_state)
            print(f"Reduce: {A} -> {' '.join(beta)}")
            logs.append(f"Reduce: {A} -> {' '.join(beta)}")

        elif action[0] == 'accept':
            print("Cadena aceptada por el analizador sintáctico.")
            return True, logs

        else:
            print(f"Error en línea {count}: acción inválida en estado {s} con símbolo '{a}'")
            logs.append(f"Error en línea {count}: acción inválida en estado {s} con símbolo '{a}'")
            return False, logs


def resolve_token_type(t):
    # Si es una palabra clave, el token que reconoce el parser es el value en sí (e.g., 'if', 'else')
    if t['type'] == 'PalabraClave':
        return t['value']
    if t['type'] == 'cadena':
        return 'cadena'
    return t['type'][0].upper() + t['type'][1:]