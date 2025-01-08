import json
import re

from transformers import AutoTokenizer, AutoModel


class CodeParserLLM:
    def __init__(self):
        # Initialize the tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        self.model = AutoModel.from_pretrained("microsoft/codebert-base")
        self.features = {}

    def parse_code(self, code, language):
        """
        Parse the provided code (and language, if specified) using the Hugging Face model to extract features.
        """
        # Tokenize the input code (max_length set to 512)
        inputs = self.tokenizer(code, return_tensors="pt", truncation=True, padding="max_length", max_length=512)

        # Generate the LLM response (prediction)
        outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state

        # Generate LLM-based insights
        generated_text = self._generate_llm_insights(embeddings)

        # Extract features using static analysis methods and dynamic analysis from the LLM
        self.features = self.extract_features(code, generated_text, language)

    def extract_features(self, code, generated_text, language):
        """
        Extract features dynamically using the LLM response and static analysis for the specified language.
        """
        features = {
            "language": language,
            "variables": self._extract_variables(code, language),
            "data_types": self._extract_data_types(code, language),
            "functions": self._extract_functions(code, language),
            "classes": self._extract_classes(code, language),
            "imports": self._extract_imports(code, language),
            "comments": self._extract_comments(code, language),
            "operators": self._extract_operators(code, language),
            "control_structures": self._extract_control_structures(code, language),
            "multithreading": self._extract_multithreading(code, language),
            # Add more extraction logic for other features as needed
        }

        # Add LLM-based insights if needed
        features["llm_analysis"] = generated_text

        return features

    def _extract_variables(self, code, language):
        """Use regex to extract variable definitions based on the language."""
        if language in ["python", "r", "js", "nodejs", "react"]:
            pattern = r"(\w+)\s*=\s*(.*)"
        elif language in ["java", "c", "cpp", "rust"]:
            pattern = r"(\w+)\s+(\w+)\s*=\s*(.*);"
        elif language in ["html", "css"]:
            return []
        else:
            return []

        variables = []
        matches = re.findall(pattern, code)
        for match in matches:
            if language in ["java", "c", "cpp", "rust"]:
                name, value = match[1], match[2]
            else:
                name, value = match[0], match[1]
            try:
                inferred_type = type(eval(value, {"__builtins__": None}, {})).__name__
            except:
                inferred_type = "unknown"
            variables.append({"name": name, "value": value.strip(), "type": inferred_type})

        return variables

    def _extract_data_types(self, code, language):
        """Detect commonly used data types based on the language."""
        if language in ["python", "js", "nodejs", "react", "r"]:
            pattern = r"\b(int|float|str|bool|list|dict|set|tuple)\b"
        elif language in ["java", "c", "cpp", "rust"]:
            pattern = r"\b(int|float|char|double|string|bool|List|Map|Set|HashMap|Vec)\b"
        elif language in ["html", "css"]:
            return []
        else:
            return []

        return re.findall(pattern, code)

    def _extract_operators(self, code, language):
        """Extract arithmetic, logical, and other operators."""
        pattern = r"(\+|-|\*|/|%|==|!=|<=|>=|&&|\|\||!|and|or|not|\+=|-=|\*=|/=|%=)"
        return re.findall(pattern, code)

    def _extract_functions(self, code, language):
        """Use regex to extract function definitions for the specified language."""
        if language in ["python", "r"]:
            func_pattern = r"def\s+(\w+)\((.*?)\):"
        elif language in ["java", "js", "nodejs", "react", "cpp", "c", "rust"]:
            func_pattern = r"(?:\w+\s+)?(\w+)\s+(\w+)\((.*?)\)\s*{"
        elif language in ["html", "css"]:
            return []
        else:
            return []

        functions = []
        matches = re.finditer(func_pattern, code)
        for match in matches:
            if language in ["java", "js", "nodejs", "react", "cpp", "c", "rust"]:
                func_name = match.group(2)
                args = match.group(3).split(",") if match.group(3) else []
            else:
                func_name = match.group(1)
                args = match.group(2).split(",") if match.group(2) else []

            func_code = code[match.start():]  # Get the function body
            func_code = func_code.split("\n\n", 1)[0]  # Assume function ends at next blank line

            return_value = None  # Java and C-style languages don't support return extraction via simple regex
            return_type = "unknown"

            if return_value:
                try:
                    return_type = type(eval(return_value, {"__builtins__": None}, {})).__name__
                except:
                    return_type = "unknown"

            functions.append({
                "name": func_name,
                "args": [arg.strip() for arg in args if arg.strip()],
                "return_statement": return_value,
                "return_type": return_type
            })

        return functions

    def _extract_classes(self, code, language):
        """Use regex to extract class definitions."""
        if language in ["python", "java", "cpp", "js", "rust", "nodejs", "react"]:
            pattern = r"class\s+(\w+)\((.*?)\):" if language == "python" else r"class\s+(\w+)\s*(?:extends\s+(\w+))?\s*{"
        elif language in ["html", "css", "r"]:
            return []
        else:
            return []

        return [{"name": match[0], "base_classes": match[1].split(",") if match[1] else []} for match in
                re.findall(pattern, code)]

    def _extract_imports(self, code, language):
        """Use regex to extract import statements for the language."""
        if language in ["python", "js", "nodejs", "react"]:
            pattern = r"import\s+(.*?)\s+(?:as\s+(.*))?$"
        elif language in ["java", "cpp", "c", "rust"]:
            pattern = r"import\s+(.*);\s*|#include\s*<(.*)>"
        elif language in ["r"]:
            pattern = r"library\((.*?)\)"
        elif language in ["html", "css"]:
            return []
        else:
            return []

        matches = re.findall(pattern, code)
        imports = []
        for match in matches:
            imports.append({"module": match[0] if match[0] else match[1], "alias": None})

        return imports

    def _extract_comments(self, code, language):
        """Extract single-line and multi-line comments for the language."""
        if language in ["python", "r", "js", "nodejs", "react"]:
            single_line_pattern = r"#.*"
            multi_line_pattern = r"\"\"\".*?\"\"\"|'''.*?'''"
        elif language in ["java", "cpp", "c", "rust"]:
            single_line_pattern = r"//.*"
            multi_line_pattern = r"/\*.*?\*/"
        elif language in ["html", "css"]:
            single_line_pattern = None
            multi_line_pattern = r"<!--.*?-->"
        else:
            return {"single_line_comments": [], "multi_line_comments": []}

        single_line_comments = re.findall(single_line_pattern, code) if single_line_pattern else []
        multi_line_comments = re.findall(multi_line_pattern, code)

        return {
            "single_line_comments": single_line_comments,
            "multi_line_comments": multi_line_comments,
        }

    def _extract_control_structures(self, code, language):
        """Identify control structures for the language."""
        if language in ["python", "r", "java", "cpp", "c", "rust", "js", "nodejs", "react"]:
            pattern = r"\b(if|else|elif|switch|case|for|while|break|continue|return|try|catch|finally|except)\b"
        elif language in ["html", "css"]:
            return []
        else:
            return []

        return re.findall(pattern, code)

    def _extract_multithreading(self, code, language):
        """Detect threading or multiprocessing usage."""
        if language in ["python"]:
            pattern = r"(threading|multiprocessing)"
        elif language in ["java", "cpp", "c", "rust"]:
            pattern = r"(Thread|ExecutorService|concurrent|thread|pthread)"
        elif language in ["js", "nodejs", "react"]:
            pattern = r"(Worker|web worker)"
        else:
            return []

        return re.findall(pattern, code)

    def _generate_llm_insights(self, embeddings):
        """Process embeddings and produce insights (placeholder logic)."""
        return "LLM-based insights extracted."

    def get_features(self):
        """Return extracted features."""
        return self.features


if __name__ == "__main__":
    with open("sampleCode.py", "r") as file:
        sample_code = file.read()

    parser = CodeParserLLM()
    parser.parse_code(sample_code, language="python")
    features = parser.get_features()

    # Save the extracted features in a readable JSON format to a file
    with open("sampleCodeFeatures.txt", "w") as output_file:
        output_file.write(json.dumps(features, indent=4))
