import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from regex_afd.utils.regex_converter import convert_to_regex, convert_to_dfa

class YALexLexer:
    def __init__(self, yalex_file):
        self.yalex_file = yalex_file
        self.tokens = []
        self.dfa = {}
        self.literal_token_map = {}
        self.actions = {}
        self.keywords = {}
        self.errors = []  

    def build_dfa(self):
        """Lee y construye el DFA a partir del archivo .yalex"""
        with open(self.yalex_file, 'r',encoding='utf-8' ) as f:
            lines = f.readlines()

        token_definitions = {}
        in_rules = False
        token_names = {}  # Mapeo dinámico de nombres de tokens

        for line in lines:
            line = line.strip()

            # Saltar comentarios o líneas vacías
            if line.startswith('(*') or line == '' or line.startswith('*)'):
                continue

            # Detectar la definición de tokens con "let"
            if line.startswith("let "):
                name, expr = line[4:].split('=', 1)
                name = name.strip()
                expr = expr.strip()

                if name == "keyword":
                    self.keywords = self.extract_keywords(expr)
                    continue

                token_definitions[name] = convert_to_regex(expr)

            # Iniciar lectura de reglas
            elif line.startswith("rule tokens ="):
                in_rules = True
                continue

            elif in_rules:
                if '|' in line:
                    token_info = line.split('|', 1)[1].strip()
                    token_def, action = token_info.split('{', 1)
                    token_def = token_def.strip()
                    action = action.strip('}').strip()

                    # Si el token es un literal como '+', '*', '='
                    if token_def.startswith("'") and token_def.endswith("'"):
                        token_def = token_def[1:-1]  # Eliminar comillas alrededor del literal

                    # Guardar el mapeo real del token
                    token_action_name = action.replace('print("', '').replace('\\n")', '').strip()

                    # Si es un símbolo especial como ':' etc., mapearlo también directo
                    if len(token_def) == 1 and token_def in ":=(){}[],;":
                        self.literal_token_map[token_def] = token_action_name

                    # Mapear siempre el nombre del token lógico también
                    token_names[token_def] = token_action_name


                    # Ignorar espacioEnBlanco para que no imprima nada
                    if token_def == "espacioEnBlanco":
                        self.actions[token_def] = "pass"
                    else:
                        self.actions[token_def] = action

                    # Construir DFA para el literal si es necesario
                    if len(token_def) == 1:
                        self.dfa[token_def] = convert_to_dfa(token_def)

        # Construcción de DFA para las expresiones regulares
        for name, expr in token_definitions.items():
            self.dfa[name] = convert_to_dfa(expr)
            token_names[name] = name  # Almacena el nombre del token

        for keyword in self.keywords:
            self.dfa[keyword] = convert_to_dfa(keyword)

            token_names[keyword] = "PalabraClave"
        

        self.token_names = token_names  # Guarda el mapeo en la instancia

    def extract_keywords(self, expr):
        """Extrae palabras clave desde el archivo YALex"""
        # Remover comillas simples y dividir por |
        expr = expr.replace("'", "").replace(" ", "")
        return expr.split('|')

    def tokenize(self, text):
        def flush_buffer():
            nonlocal buffer, token_type
            if buffer:
                if token_type == "letra":
                    if buffer in self.keywords:
                        print("PalabraClave")
                        self.tokens.append({"type": "PalabraClave", "value": buffer})
                    else:
                        token_name = self.token_names.get("identificador", "identificador")
                        print(token_name)
                        self.tokens.append({"type": token_name, "value": buffer})
                elif token_type == "digito":
                    token_name = self.token_names.get("numero", "numero")
                    print(token_name)
                    self.tokens.append({"type": token_name, "value": buffer})
                buffer = ""
                token_type = None

        pos = 0
        buffer = ""
        token_type = None
        self.tokens = []

        while pos < len(text):
            # — Detectar cadenas antes que todo —
            if text[pos] == '"':
                end_pos = pos + 1
                while end_pos < len(text) and text[end_pos] != '"':
                    end_pos += 1
                if end_pos < len(text):  # cadena cerrada
                    match = text[pos:end_pos + 1]
                    flush_buffer()
                    print("cadena")
                    self.tokens.append({"type": "cadena", "value": match})
                    pos = end_pos + 1
                    continue
                else:
                    self.errors.append(f"Cadena sin cerrar desde posición {pos}")
                    pos += 1
                    continue

            # — Detectar números decimales manualmente —
            if text[pos].isdigit():
                start = pos
                while pos < len(text) and text[pos].isdigit():
                    pos += 1
                if pos < len(text) and text[pos] == '.' and pos + 1 < len(text) and text[pos + 1].isdigit():
                    pos += 1
                    while pos < len(text) and text[pos].isdigit():
                        pos += 1
                    match = text[start:pos]
                    flush_buffer()
                    print("numero")
                    self.tokens.append({"type": "numero", "value": match})
                    continue
                pos = start  # no era decimal, retrocede

            # — Verificar tokens compuestos o literales —
            max_len = min(6, len(text) - pos)
            for length in range(max_len, 0, -1):
                possible_token = text[pos:pos + length]
                if possible_token in self.literal_token_map:
                    flush_buffer()
                    token_type = self.literal_token_map[possible_token]
                    print(token_type)
                    self.tokens.append({"type": token_type, "value": possible_token})
                    pos += length
                    token_type = None
                    break
                if possible_token in self.token_names:
                    flush_buffer()
                    token_type = self.token_names[possible_token]
                    print(token_type)
                    self.tokens.append({"type": token_type, "value": possible_token})
                    pos += length
                    token_type = None
                    break
            else:
                match, current_type = self.match_token(text, pos)

                if current_type in ["letra", "digito"]:
                    buffer += match
                    if token_type is None:
                        token_type = "letra" if current_type == "letra" else "digito"
                    pos += len(match)
                    continue

                if match in [' ', '\t', '\n']:
                    flush_buffer()
                    pos += 1
                    continue

                flush_buffer()
                if match and current_type in self.actions:
                    action = self.actions[current_type]
                    if action not in ("pass", "{}"):
                        print(action.replace('print(\"', '').replace('\\n\")', '').strip())
                        self.tokens.append({"type": current_type, "value": match})
                elif match and current_type not in ["espacio", "delimitador"]:
                    print(current_type)
                    self.tokens.append({"type": current_type, "value": match})

                if match:
                    pos += len(match)
                else:
                    if text[pos] not in ['\n', '\t', ' ']:
                        self.errors.append(f"Error léxico en posición {pos}: {text[pos]}")
                    pos += 1

        flush_buffer()
        return self.tokens






    def match_token(self, text, pos):
        """Compara y devuelve el token encontrado"""
        # Verificar primero si hay un token de múltiples caracteres (compuesto)
        if pos + 1 < len(text):
            possible_two_chars = text[pos:pos + 2]

            # Verificar `==` primero antes de procesar `=`
            if possible_two_chars == "==":
                return "==", "Operador de igualdad"

        # Verificar `=`, si no hay `==`
        if text[pos] == "=":
            return "=", "Operador de asignacion"

        # Verificación normal para otros tokens
        max_len = min(3, len(text) - pos)
        for length in range(max_len, 0, -1):
            possible_token = text[pos:pos + length]
            if possible_token in self.token_names:
                token_type = self.token_names[possible_token]
                return possible_token, token_type

        # Verificación estándar si no se encuentra ningún token
        for token_type in sorted(self.dfa, key=lambda x: 0 if x == "decimal" else 1):
            dfa = self.dfa[token_type]
            if token_type != "espacio":  # Saltar espacios
                match_length = self.run_dfa(dfa, text, pos)
                if match_length > 0:
                    match = text[pos:pos + match_length]

                    # Priorizar palabras clave antes de identificadores
                    if token_type == "identificador" and match in self.keywords:
                        return match, "PalabraClave"

                    token_name = self.token_names.get(token_type, token_type)
                    return match, token_name

        return None, None




    def run_dfa(self, dfa, text, pos):
        """Ejecuta el DFA para comparar el texto"""
        current_state = frozenset([0])
        match_length = 0

        for i in range(pos, len(text)):
            char = text[i]
            if (current_state, char) in dfa:
                current_state = dfa[(current_state, char)]
                match_length += 1
            else:
                break

        return match_length
