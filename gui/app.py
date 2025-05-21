import streamlit as st

st.set_page_config(page_title="YALex/YAPar Generator", layout="centered")

st.title("YALex / YAPar Generator UI")

# Dropdown for selecting example type
example_type = st.selectbox(
    "Choose YALex Specification Type:",
    options=["Easy", "Hard", "Complex"]
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
