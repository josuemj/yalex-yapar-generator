from graphviz import Digraph
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.lexer import YALexLexer
from regex_afd.model.afn_afd import direct_method
from regex_afd.utils.regex_converter import convert_to_regex


def visualize_automaton(lexer: YALexLexer):
    """Grafica AFD"""

    token_definitions = {}
    with open(lexer.yalex_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line.startswith("let "):
            name, expr = line[4:].split('=', 1)
            token_definitions[name.strip()] = expr.strip()

    def resolve(expr):
        for key in sorted(token_definitions.keys(), key=lambda x: -len(x)):
            expr = expr.replace(key, f"({token_definitions[key]})")
        return expr

    dfa_list = []
    token_names = []

    for name, raw_expr in token_definitions.items():
        try:
            resolved = resolve(raw_expr)
            regex = convert_to_regex(resolved)
            dfa = direct_method(regex)
            dfa_list.append(dfa)
            token_names.append(name)
        except Exception as e:
            print(f"Error en token '{name}': {e}")

    def merge_dfas(dfa_list, token_names):
        merged = {}
        offset = 1
        start_state = frozenset([0])

        for i, dfa in enumerate(dfa_list):
            mapping = {}
            token = token_names[i]

            for (src, c), dst in dfa.items():
                new_src = frozenset(s + offset for s in src)
                new_dst = frozenset(s + offset for s in dst)
                merged[(new_src, c)] = new_dst

                for s in src:
                    mapping[s] = s + offset
                for s in dst:
                    mapping[s] = s + offset

            if mapping:
                entry_state = frozenset([mapping[0]])
                merged[(start_state, f"#START_{token}")] = entry_state
                offset = max(mapping.values()) + 1

        return merged

    global_dfa = merge_dfas(dfa_list, token_names)

    def get_reachable_states(dfa, start=frozenset([0])):
        reachable = set()
        queue = [start]

        while queue:
            current = queue.pop(0)
            if current in reachable:
                continue
            reachable.add(current)
            for (src, _), dst in dfa.items():
                if src == current and dst not in reachable:
                    queue.append(dst)

        return reachable

    reachable_states = get_reachable_states(global_dfa)

    dot = Digraph(name="GlobalAFD")
    dot.attr(rankdir='LR')

    for s in reachable_states:
        node_attrs = {'shape': 'circle', 'style': 'filled', 'fillcolor': 'white'}
        if s == frozenset([0]):
            node_attrs.update({'shape': 'doublecircle', 'fillcolor': 'green'})
        dot.node(str(s), **node_attrs)

    for (src, c), dst in global_dfa.items():
        if src in reachable_states and dst in reachable_states:
            label = c.replace("\\", "\\\\").replace('"', '\\"')
            dot.edge(str(src), str(dst), label=label)

    print("Total DFA transitions:", len(global_dfa))
    print("DFA transitions preview:", list(global_dfa.items())[:5])
    dot.render("AFD_Global", format='pdf', view=True)
