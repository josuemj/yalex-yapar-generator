from graphviz import Digraph
from yapar.automaton.token_map import TOKEN_MAP

def escape_html(text):
    """Escapa caracteres especiales para Graphviz HTML."""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
            .replace("~", "&#126;")  # ← escape del punto
    )

def render_automaton(automaton, output_path='output/automaton', format='png'):
    dot = Digraph(comment="LR(0) Automaton", format=format)
    dot.attr(rankdir='LR')
    dot.attr('node', shape='plaintext', fontname='Courier')

    for idx, state in enumerate(automaton.states):
        core_items = automaton.core_items.get(idx, set())

        core_lines = []
        closure_lines = []

        for item in state:
            line = escape_html(str(item))
            if item in core_items:
                # Color azul oscuro y negrita
                core_lines.append(
                    f"<TR><TD ALIGN='LEFT'><FONT COLOR='#003366'><B>{line}</B></FONT></TD></TR>"
                )
            else:
                closure_lines.append(f"<TR><TD ALIGN='LEFT'>{line}</TD></TR>")

        label = f"""<
        <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0">
            <TR><TD ALIGN="CENTER" BGCOLOR="#eeeeee"><B>I{idx}</B></TD></TR>
            {''.join(core_lines)}
            {''.join(closure_lines)}
        </TABLE>
        >"""

        dot.node(str(idx), label)

    for (src, sym), dst in automaton.transitions.items():
        label = TOKEN_MAP.get(sym, sym)
        label = escape_html(label)
        dot.edge(str(src), str(dst), label=label)

    dot.render(output_path, cleanup=True)