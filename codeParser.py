import ast

class CodeParser(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []
        self.imports = []
        self.variables = []
        self.comments = []
        self.docstrings = []
        self.code = []

    def visit_FunctionDef(self, node):
        docstring = ast.get_docstring(node)
        returnAnnotation = None

        # Analyze return type annotations
        if node.returns:
            try:
                returnAnnotation = ast.unparse(node.returns)  # For explicit annotations
            except AttributeError:
                returnAnnotation = getattr(node.returns, "id", None)

        # Infer return type by analyzing return statements
        if not returnAnnotation:
            inferred_return_types = set()
            for body_node in node.body:
                if isinstance(body_node, ast.Return):
                    if isinstance(body_node.value, ast.Constant):
                        inferred_return_types.add(type(body_node.value.value).__name__)
                    elif isinstance(body_node.value, ast.Name):
                        inferred_return_types.add("variable")
                    elif isinstance(body_node.value, ast.Call):
                        inferred_return_types.add("function_call")
                    else:
                        inferred_return_types.add("unknown")

            if inferred_return_types:
                returnAnnotation = ", ".join(inferred_return_types)
                
        function_info = {
            "name": node.name,
            "docstring": docstring,
            "args": [arg.arg for arg in node.args.args],
            "returns": returnAnnotation
        }
        self.functions.append(function_info)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        docstring = ast.get_docstring(node)
        class_info = {
            "name": node.name,
            "base_classes": [base.id for base in node.bases if hasattr(base, "id")],
            "docstring": docstring,
            "methods": []
        }
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_docstring = ast.get_docstring(item)
                method_info = {
                    "name": item.name,
                    "args": [arg.arg for arg in item.args.args],
                    "docstring": method_docstring
                }
                class_info["methods"].append(method_info)
        self.classes.append(class_info)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append({"module": alias.name, "alias": alias.asname})

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.append({"module": node.module, "alias": alias.name})

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables.append({"name": target.id, "value": ast.dump(node.value)})
        self.generic_visit(node)

    def parse_comments(self, code):
        lines = code.splitlines()
        is_multiline = False
        multiline_buffer = []

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("#"):
                self.comments.append(stripped)
            elif stripped.startswith('"""'):
                if is_multiline:
                    multiline_buffer.append(stripped)
                    self.comments.append("\n".join(multiline_buffer))
                    multiline_buffer = []
                    is_multiline = False
                else:
                    is_multiline = True
                    multiline_buffer.append(stripped)
            elif stripped.startswith('"""') and stripped.endswith("'''"):
                if not is_multiline:
                    self.comments.append(stripped)
            elif is_multiline:
                multiline_buffer.append(stripped)

    def parse(self, code):
        self.code = code.splitlines()
        try:
            tree = ast.parse(code)
            self.visit(tree)
        except SyntaxError as e:
            print(f"SyntaxError in parsing: {e}")
        self.parse_comments(code)

if __name__ == "__main__":
    with open("sampleCode.py", "r") as file:
        sampleCode = file.read()

    parser = CodeParser()
    parser.parse(sampleCode)
    print("Functions:", parser.functions)
    print("Classes:", parser.classes)
    print("Imports:", parser.imports)
    print("Variables:", parser.variables)
    print("Comments:", parser.comments)
    print("Docstrings:", parser.docstrings)