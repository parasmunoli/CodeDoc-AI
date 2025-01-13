import ast
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class CodeFeatureExtractor(ast.NodeVisitor):
    def __init__(self, program_name="Program Analysis"):
        self.program_name = program_name
        self.features = {
            "Classes": [],
            "Functions": [],
            "Error Handling": [],
            "Input Handling": [],
            "User Interaction": [],
            "Program Flow": [],
            "Mathematical Operations": []
        }
        self.variable_types = {}  # To store variable names and types

    def visit_ClassDef(self, node):
        class_info = {"name": node.name, "description": "", "methods": []}
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = {"name": item.name, "description": ""}
                class_info["methods"].append(method_info)
        self.features["Classes"].append(class_info)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        function_info = {"name": node.name, "description": ""}
        self.features["Functions"].append(function_info)
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                if isinstance(node.value, ast.Constant):
                    data_type = type(ast.literal_eval(node.value))
                else:
                    data_type = "Unknown"
                self.variable_types[target.id] = str(data_type)
        self.generic_visit(node)

    def extract(self, code):
        try:
            tree = ast.parse(code)
            self.visit(tree)
            return self.features, self.variable_types
        except Exception as e:
            print(f"Error parsing code: {e}")
            return {}, {}


class CodeAnalysis:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("t5-small")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

    def analyze_code(self, code):
        parser = CodeFeatureExtractor()
        features, variables = parser.extract(code)

        # Use T5 to generate descriptions
        for cls in features["Classes"]:
            cls["description"] = self.generate_detailed_documentation(cls["name"], "class")
            for method in cls["methods"]:
                method["description"] = self.generate_detailed_documentation(method["name"], "method")

        for func in features["Functions"]:
            func["description"] = self.generate_detailed_documentation(func["name"], "function")

        # Return results in the desired format
        return {
            "program": "Arithmetic and Advanced Arithmetic Operations",
            "features": features,
            "variables": variables
        }

    def generate_detailed_documentation(self, name, entity_type):
        """
        Generate detailed documentation using LLM.
        """
        prompt = (
            f"Write a detailed and well-structured documentation for a {entity_type} named '{name}' in a Python program. "
            f"Provide an overview of its purpose, specific use cases, interaction with other components, methods or functionalities it contains, "
            f"and any example use. Follow a structured format similar to professional software documentation."
        )
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model.generate(**inputs, max_length=200, num_beams=5, early_stopping=True)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


if __name__ == "__main__":
    # Read the sample code from file
    with open("sampleCode.py", "r") as file:
        sample_code = file.read()

    # Analyze the code
    print("Analyzing code...")
    analyzer = CodeAnalysis()
    result = analyzer.analyze_code(sample_code)
    print("Analysis complete.")

    print("Saving results to JSON file...")
    # Save results as a JSON file
    with open("sampleAnalysis.json", "w") as file:
        json.dump(result, file, indent=4)

    print("Results saved to JSON file.")

    print("Generating detailed documentation...")
    # Generate a detailed documentation markdown file
    with open("detailedDocumentation.md", "w") as doc_file:
        doc_file.write(f"# Program Name: {result['program']}\n\n")
        doc_file.write("## Extracted Features and Documentation\n\n")

        for cls in result["features"]["Classes"]:
            doc_file.write(f"### Class: {cls['name']} : \n")
            doc_file.write(f"{cls['description']}\n\n")
            doc_file.write("#### Methods:\n")
            for method in cls["methods"]:
                doc_file.write(f"#### `{method['name']}` : \n")
                doc_file.write(f"{method['description']}\n")
            doc_file.write("\n")

        doc_file.write("#### Functions:\n")
        for func in result["features"]["Functions"]:
            doc_file.write(f"#### `{func['name']}` : \n")
            doc_file.write(f"**Description**: {func['description']}\n\n")

        doc_file.write("## Variable Types\n")
        for var, var_type in result["variables"].items():
            doc_file.write(f"- `{var}`: {var_type}\n")

    print("Detailed documentation generated.")