from core.parser.python_parser import parse_file, get_source
from core.docstring_engine.llm_integration import generate_ai_doc


def review_file(file_path):
    functions = parse_file(file_path)

    results = []

    for func in functions:
        if func["docstring"] is None:
            code = get_source(file_path, func["node"])
            doc = generate_ai_doc(code)

            results.append({
                "function": func["name"],
                "doc": doc
            })

    return results