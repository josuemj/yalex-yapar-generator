import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st

# Utils
from utils.parser_utils import parse_yapar_file
from yapar.utils.first import compute_first
from yapar.utils.follow import compute_follow
from yapar.utils.build_slr_table import build_slr_table

st.set_page_config(page_title="YALex/YAPar Generator", layout="centered")

st.title("YALex / YAPar Generator UI")

# Dropdown for selecting example type
example_type = st.selectbox(
    "Choose YALex Specification Type:",
    options=["easy", "hard", "complex"]
)


# Text input area for writing or editing the specification
spec_input = st.text_area(
    "code",
    height=300,
    placeholder="Type or paste your specification here..."
)

# Run button
if st.button("Run"):
    st.success(f"to implement")
