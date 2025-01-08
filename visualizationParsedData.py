import streamlit as st
import json
from codeParser import CodeParser  # Assuming your parser is saved in `code_parser.py`


def parse_and_display_code(fileContent):
    # Parse code
    parser = CodeParser()
    parser.parse(fileContent)

    # Display parsed data
    st.header("Parsed Code Features")

    # Display Functions
    with st.expander("Functions"):
        st.json(parser.functions)

    # Display Classes
    with st.expander("Classes"):
        st.json(parser.classes)

    # Display Variables
    with st.expander("Variables"):
        st.json(parser.variables)

    # Display Imports
    with st.expander("Imports"):
        st.json(parser.imports)

    # Display Comments
    with st.expander("Comments"):
        st.json(parser.comments)


# Streamlit App
st.title("Code Parsing Dashboard")

# File Upload
uploaded_file = st.file_uploader("Upload a code file", type=["py", "js", "java", "cpp", "cs"])
if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8")
    st.text_area("Uploaded Code", file_content, height=300)
    parse_and_display_code(file_content)
