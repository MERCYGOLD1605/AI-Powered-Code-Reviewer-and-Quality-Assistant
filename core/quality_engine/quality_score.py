def calculate_quality_score(functions):

    if not functions:
        return {
            "coverage": 0,
            "naming": 0,
            "args": 0,
            "overall": 0
        }

    total_functions = len(functions)

    # -------------------
    # Docstring Coverage
    # -------------------
    documented = sum(
        1 for f in functions
        if f["docstring"]
    )

    coverage_score = (
        documented / total_functions
    ) * 100

    # -------------------
    # Function Naming
    # -------------------
    bad_names = {
        "a",
        "abc",
        "test",
        "temp",
        "x",
        "y",
        "func"
    }

    good_names = sum(
        1
        for f in functions
        if f["name"].lower() not in bad_names
        and len(f["name"]) > 2
    )

    naming_score = (
        good_names / total_functions
    ) * 100

    # -------------------
    # Arguments Score
    # -------------------
    argument_score = 100

    for f in functions:
        if len(f["args"]) > 5:
            argument_score -= 10

    argument_score = max(argument_score, 0)

    # -------------------
    # Overall Score
    # -------------------
    overall_score = round(
        (
            coverage_score +
            naming_score +
            argument_score
        ) / 3
    )

    return {
        "coverage": round(coverage_score),
        "naming": round(naming_score),
        "args": round(argument_score),
        "overall": overall_score
    }