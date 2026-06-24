def generate_basic_doc(name, args):
    args_section = "\n".join([f"    {a}: description" for a in args])

    return f'''"""{name} function.

Args:
{args_section}

Returns:
    description
"""'''