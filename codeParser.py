import ast

class CodeParser(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []
        self.imports = []
        self.variables = []
        self.comments = []
        self.docStrings = []
        self.code = []

    def visitFunctionDef(self, node):
        docString = ast.get_docstring(node)
        functionInfo = {
            "name": node.name,
            "docString": docString,
            "args": [arg.arg for arg in node.args.args],
            "returns": getattr(node.returns, "id", None) if node.returns else None
        }
        self.functions.append(functionInfo)
        self.generic_visit(node)

