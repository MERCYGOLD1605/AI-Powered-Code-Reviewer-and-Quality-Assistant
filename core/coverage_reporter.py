def generate_report(functions):
    total = len(functions)
    with_doc = sum(1 for f in functions if f["docstring"])

    return {
        "total": total,
        "with_doc": with_doc,
        "coverage": (with_doc / total * 100) if total else 0
    }