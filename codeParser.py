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


