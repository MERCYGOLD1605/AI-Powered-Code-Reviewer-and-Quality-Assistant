def detect_code_smells(functions):

    smells = []

    generic_names = {
        "test",
        "temp",
        "abc",
        "a",
        "x",
        "y",
        "func"
    }

    for func in functions:

        # Missing docstring
        if not func["docstring"]:
            smells.append(
                f"⚠ Missing docstring: {func['name']}"
            )

        # Generic names
        if func["name"].lower() in generic_names:
            smells.append(
                f"⚠ Generic function name: {func['name']}"
            )

        # Too many arguments
        if len(func["args"]) > 5:
            smells.append(
                f"⚠ Too many arguments: {func['name']}"
            )

    return smells