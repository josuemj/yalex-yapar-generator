import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st

# Utils
from utils.parser_utils import parse_yapar_file
from yapar.utils.first import compute_first
from yapar.utils.follow import compute_follow
from yapar.utils.build_slr_table import build_slr_table
from yapar.visualizer import render_automaton
from yapar.build_automaton import build_from_grammar
from yapar.utils.parse_driver import parse_tokens, resolve_token_type

from yalex.src.lexer import YALexLexer

st.set_page_config(page_title="YALex/YAPar Generator", layout="centered")

st.title("YALex / YAPar Generator UI")

example_type = st.selectbox("Choose Specification Type:", options=["easy", "hard", "complex"])

input_string = st.text_area("Input string to analyze:", placeholder="Write a program or expression to test...", height=200)

# Checkboxes para mostrar info
show_automaton = st.checkbox("Show SLR Automaton", value=True)
show_tokens = st.checkbox("Show Tokens", value=True)
show_first_follow = st.checkbox("Show FIRST & FOLLOW", value=True)
show_tables = st.checkbox("Show ACTION & GOTO Tables", value=True)
show_phases = st.checkbox("Show SHIFT & REDUCE Tables", value=True)

if st.button("Run"):
    selected_type = example_type
    st.write(f"Running for: `{selected_type}`")

    # Load YAPAR grammar
    parsed = parse_yapar_file(f'../examples/yapar/{selected_type}.yalp')
    grammar = parsed['grammar']
    terminals = parsed['terminales']
    start_symbol = 'Program'

    # FIRST & FOLLOW
    first = compute_first(grammar, terminals)
    follow = compute_follow(grammar, terminals, first, start_symbol)

    if show_first_follow:
        st.subheader("FIRST Sets")
        for nt, f in first.items():
            if nt in grammar:
                st.write(f"**FIRST({nt})** = {f}")

        st.subheader("FOLLOW Sets")
        for nt, f in follow.items():
            st.write(f"**FOLLOW({nt})** = {f}")

    # Automaton
    automaton = build_from_grammar(parsed)
    if show_automaton:
        st.subheader("SLR Automaton")
        render_automaton(automaton, output_path='output/automaton', format='png')
        st.image("output/automaton.png", caption="SLR Automaton")

    # ACTION and GOTO tables
    ACTION, GOTO = build_slr_table(automaton, grammar, terminals, follow, start_symbol)

    if show_tables:
        st.subheader("ACTION Table")
        for state, actions in ACTION.items():
            for symbol, action in actions.items():
                st.write(f"ACTION[{state}, {symbol}] = {action}")

        st.subheader("GOTO Table")
        for state, transitions in GOTO.items():
            for symbol, next_state in transitions.items():
                st.write(f"GOTO[{state}, {symbol}] = {next_state}")

    # YALEX Lexer
    yalex_file = f"../examples/yalex/{selected_type}.yalex"
    lexer = YALexLexer(yalex_file)
    lexer.build_dfa()

    if input_string.strip():
        lexer.tokenize(input_string)

        if show_tokens:
            st.subheader("Generated Tokens")
            for tok in lexer.tokens:
                st.write(tok)

        tokens = [(resolve_token_type(t), t['value']) for t in lexer.tokens]

        # Add EOF
        if not tokens or tokens[-1][0] != '$':
            tokens.append(('$', '$'))

        st.subheader("SLR Parsing Result")
        success, logs = parse_tokens(tokens, ACTION, GOTO, count=1, start_symbol=start_symbol)

        if show_phases:
            for line in logs:
                st.text(line)

        if success:
            st.success("✅ Input accepted by the parser.")
        else:
            st.error("❌ Input rejected by the parser.")

        if lexer.errors:
            st.subheader("Lexical Errors")
            for error in lexer.errors:
                st.error(error)
    else:
        st.warning("Please provide an input string to analyze.")