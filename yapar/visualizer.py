from graphviz import Digraph
from yapar.automaton.token_map import TOKEN_MAP

def render_automaton(automaton, output_path='output/automaton', format='png'):
    dot = Digraph(comment="LR(0) Automaton", format=format)
    dot.attr(rankdir='LR')

    # Añadir nodos (estados)
    for idx, state in enumerate(automaton.states):
        label = f"I{idx}:\n" + '\n'.join(str(item) for item in state)
        dot.node(str(idx), label, shape='box')

    # Añadir transiciones
    for (src, sym), dst in automaton.transitions.items():
        label = TOKEN_MAP.get(sym, sym)
        dot.edge(str(src), str(dst), label=label)

    dot.render(output_path, cleanup=True)