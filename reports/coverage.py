def generate_coverage_report(functions):
    total = len(functions)
    with_doc = sum(
        1 for f in functions
        if f["docstring"]
    )

    missing = total - with_doc

    return {
        "total": total,
        "with_doc": with_doc,
        "missing": missing,
        "coverage": round(
            (with_doc / total * 100)
            if total else 0,
            2
        )
    }