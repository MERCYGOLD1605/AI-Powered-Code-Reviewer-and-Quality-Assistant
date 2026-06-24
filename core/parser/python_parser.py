import ast

class PythonParser(ast.NodeVisitor):
    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):
        self.functions.append({
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "docstring": ast.get_docstring(node),
            "lineno": node.lineno,
            "node": node
        })
        self.generic_visit(node)


def parse_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    parser = PythonParser()
    parser.visit(tree)

    return parser.functions


def get_source(file_path, node):
    with open(file_path, "r") as f:
        lines = f.readlines()

    return "".join(lines[node.lineno - 1: node.end_lineno])