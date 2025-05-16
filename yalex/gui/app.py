import streamlit as st
import os
import sys
import tempfile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.lexer import YALexLexer
from regex_afd.utils.visualizer import visualize_automaton

# Configuración de la página
st.set_page_config(page_title="YALex Lexer", layout="centered")

# Título principal
st.title("Analizador Léxico con YALex")

# Sección para seleccionar o subir el archivo YALex
st.markdown("### Seleccionar las reglas (.yalex, arrastrar)")
yalex_file = st.file_uploader("Subir archivo YALex", type=["yalex"])

# Mostrar nombre del archivo si se selecciona
if yalex_file:
    st.success(f"Archivo seleccionado: {yalex_file.name}")
    yalex_content = yalex_file.read().decode("utf-8")
    st.text_area("Contenido del archivo YALex", yalex_content, height=300)
    
    yalex_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".yalex", mode="w", encoding="utf-8")
    yalex_temp.write(yalex_content)
    yalex_temp.close()
    yalex_path = yalex_temp.name
else:
    st.warning("No se ha seleccionado ningún archivo YALex.")

# Sección para el codespace
st.markdown("### Codespace")
code_input = st.text_area(
    "Escribe el código aquí para analizarlo",
    height=200,
    placeholder="Escribe tu código aquí..."
)

# Botón para ejecutar el analizador léxico
if st.button("▶️ Run"):
    if not yalex_path:
        st.error("Primero debes subir un archivo .yalex.")
    elif not code_input.strip():
        st.error("Debes escribir código en el área de texto.")
    else:
        try:
            # Crear lexer y construir AFD
            lexer = YALexLexer(yalex_path)
            lexer.build_dfa()
            # visualize_automaton(lexer)  # Se guarda la imagen

            # Analizar entrada
            lexer.tokenize(code_input)

            st.success("✅ Análisis completado")

            # Mostrar tokens
            st.markdown("### 📜 Tokens reconocidos")
            if lexer.tokens:
                for token in lexer.tokens:
                    st.code(str(token))
            else:
                st.warning("No se reconocieron tokens.")

            # Mostrar errores
            if lexer.errors:
                st.markdown("### ❌ Errores léxicos detectados")
                for err in lexer.errors:
                    st.error(err)
            else:
                st.success("✅ Sin errores léxicos")

        except Exception as e:
            st.exception(f"Ocurrió un error al ejecutar el analizador: {e}")


