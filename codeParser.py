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
        function_info = {
            "name": node.name,
            "docstring": docstring,
            "args": [arg.arg for arg in node.args.args],
            "returns": getattr(node.returns, "id", None) if node.returns else None
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


