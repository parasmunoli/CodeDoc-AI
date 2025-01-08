import streamlit as st
import json
from llmParser import CodeParserLLM  # Assuming the code is saved in `code_parser_llm.py`

def visualize_parsed_features(code, language):
    """
    Parse the code using CodeParserLLM and visualize the extracted features.
    """
    # Initialize the parser
    parser = CodeParserLLM()
    parser.parse_code(code, language)

    # Get extracted features
    features = parser.get_features()

    # Display the features
    st.header("Parsed Code Features")

    # Display language
    st.subheader("Programming Language")
    st.write(features.get("language", "Unknown"))

    # Display Variables
    with st.expander("Variables"):
        st.json(features.get("variables", []))

    # Display Data Types
    with st.expander("Data Types"):
        st.json(features.get("data_types", []))

    # Display Functions
    with st.expander("Functions"):
        st.json(features.get("functions", []))

    # Display Classes
    with st.expander("Classes"):
        st.json(features.get("classes", []))

    # Display Imports
    with st.expander("Imports"):
        st.json(features.get("imports", []))

    # Display Comments
    with st.expander("Comments"):
        st.json(features.get("comments", {}))

    # Display Operators
    with st.expander("Operators"):
        st.json(features.get("operators", []))

    # Display Control Structures
    with st.expander("Control Structures"):
        st.json(features.get("control_structures", []))

    # Display Multithreading
    with st.expander("Multithreading"):
        st.json(features.get("multithreading", []))

    # Display LLM Analysis
    with st.expander("LLM Analysis"):
        st.write(features.get("llm_analysis", "No insights available."))

# Streamlit App
st.title("Code Analysis Dashboard")

# File Upload
uploaded_file = st.file_uploader("Upload a code file", type=["py", "java", "cpp", "js"])
if uploaded_file is not None:
    # Read file content
    code = uploaded_file.read().decode("utf-8")
    st.text_area("Uploaded Code", code, height=300)

    # Select programming language
    language = st.selectbox("Select the programming language", ["python", "java", "cpp", "js", "r", "html", "css", "nodejs", "react", "rust"])

    # Visualize parsed features
    visualize_parsed_features(code, language)
