def parse_tokens(tokens, action_table, goto_table, start_symbol):
    stack = [0]  # pila de estados
    index = 0    # índice del token actual
    a = tokens[index][0] if tokens else '$'  # ← Hacer que 'a' sea el primer símbolo de w$

    while True:
        # ← repetir indefinidamente
        s = stack[-1]  # ← hacer que 's' sea el estado en la parte superior de la pila

        # Acción a tomar
        action = action_table.get(s, {}).get(a)

        if action is None:
            print(f"Error sintáctico: no hay acción definida para estado {s} y símbolo '{a}'")
            return False

        if action[0] == 'shift':
            # ← if ACCION[s,a] = desplazar t
            t = action[1]
            stack.append(t)  # ← meter t en la pila
            index += 1
            a = tokens[index][0] if index < len(tokens) else '$'  # ← hacer que 'a' sea el siguiente símbolo
        elif action[0] == 'reduce':
            # ← else if ACCION[s,a] = reducir A → β
            A, beta = action[1], action[2]
            for _ in beta:
                stack.pop()  # ← sacar |β| símbolos de la pila
            t = stack[-1]  # ← hacer que el estado t ahora esté en la cima de la pila
            goto_state = goto_table.get(t, {}).get(A)
            if goto_state is None:
                print(f"Error: no hay transición GOTO[{t}, {A}]")
                return False
            stack.append(goto_state)  # ← meter ir_A[t,A] en la pila
            print(f"Reduce: {A} -> {' '.join(beta)}")  # ← enviar de salida la producción
        elif action[0] == 'accept':
            # ← else if ACCION[s,a] = aceptar
            print("Cadena aceptada por el analizador sintáctico.")
            return True
        else:
            # ← else llamar a la rutina de recuperación de errores
            print(f"Error: acción inválida en estado {s} con símbolo '{a}'")
            return False

def resolve_token_symbol(t):
    if t['type'] == 'PalabraClave':
        return f"PalabraClave_{t['value'].upper()}"  # Ej: 'if' -> 'PalabraClave_IF'
    return t['type']