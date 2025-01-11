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
            cls["description"] = self.generate_description(cls["name"], "class")
            for method in cls["methods"]:
                method["description"] = self.generate_description(method["name"], "method")

        for func in features["Functions"]:
            func["description"] = self.generate_description(func["name"], "function")

        # Return results in the desired format
        return {
            "program": "Arithmetic and Advanced Arithmetic Operations",
            "features": features,
            "variables": variables
        }

    def generate_description(self, name, entity_type):
        prompt = f"Describe the purpose of the {entity_type} named '{name}' in a Python program."
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model.generate(**inputs, max_length=50, num_beams=2, early_stopping=True)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    with open("sampleCode.py", "r") as file:
        sample_code = file.read()

    analyzer = CodeAnalysis()
    result = analyzer.analyze_code(sample_code)
    print(json.dumps(result, indent=4))
    with open("sampleAnalysis.json", "w") as file:
        json.dump(result, file, indent=4)