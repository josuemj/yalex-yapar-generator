# YALex-YAPar Parser Generator

This project is a syntax analyzer generator that implements a complete compilation phase using custom tools: **YALex** (for lexical analysis) and **YAPar** (for syntax analysis). It builds LR(0) automata and SLR(1) parsing tables to validate input strings against a defined grammar.

## 📁 Project Structure

```
.
│   .gitignore         # Files/folders to ignore in version control
│   main.py            # Entry point to run the whole system
│   readme.md          # Project documentation
│
├───gui/               # Graphical User Interface implementation
├───input/             # .yalex, .yapar and input string files (esay, medium, hard etc)
├───output/            # Visual outputs, parse results, errors, automata
├───yalex/             # Lexical analyzer (YALex)
└───yapar/             # Syntax analyzer (YAPar)
        yapar.p        # YAPar core logic
```

## 🚀 How to Run

```bash
python main.py 
streamlit run gui/app.py
```

Make sure your input files (.yalex, .yapar, and test strings) are placed in the `/input` folder.

## 📌 Features

- Token generation from custom regex definitions (YALex)
- LR(0) automaton construction
- SLR(1) parsing table generation
- Syntax validation for input strings
- Error reporting
- GUI for interaction and visualization

## 📂 Inputs & Outputs

- Input files go in the `/input` folder.
- Output files and visualizations will appear in `/output`.

## ✅ Requirements

- Python 3.8+
- (Optional) `graphviz` for automata visualization

---

## 📚 Notes

- Do **not** use regex libraries — pattern recognition is done via finite automata as required.
- GUI must be functional and user-friendly as part of the evaluation.
