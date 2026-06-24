import os
import argparse

from core.parser.python_parser import parse_file
from generator.docstring_generator import generate_docstring
from reports.coverage import generate_coverage_report
from core.quality_engine.quality_score import calculate_quality_score
from core.smell_engine.code_smells import detect_code_smells


def scan_directory(path, style):
    all_functions = []

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                functions = parse_file(file_path)

                print(f"\n File: {file}")

                for func in functions:
                    if func["docstring"] is None:
                        print(f"⚠ Missing docstring: {func['name']}")

                        generated = generate_docstring(
                            func["name"],
                            func["args"],
                            style
                        )

                        print("💡 Suggested Docstring:")
                        print(generated)

                all_functions.extend(functions)

    return all_functions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        help="Path to project"
    )

    parser.add_argument(
        "--style",
        default="google",
        help="Docstring style"
    )

    args = parser.parse_args()

    print("\n Scanning project...\n")

    functions = scan_directory(
        args.path,
        args.style
    )

    report = generate_coverage_report(functions)
    quality = calculate_quality_score(functions)
    smells = detect_code_smells(functions)

    print("\n" + "=" * 50)
    print("QUALITY REPORT")
    print("=" * 50)

    print(f"Coverage Score  : {quality['coverage']}")
    print(f"Naming Score    : {quality['naming']}")
    print(f"Arguments Score : {quality['args']}")
    print(f"Overall Score   : {quality['overall']}/100")

    print("\n" + "=" * 50)
    print("⚠ CODE SMELLS")
    print("=" * 50)

    if not smells:
        print("✅ No code smells detected!")
    else:
        for smell in smells:
            print(smell)

    print("\n" + "=" * 50)
    print("COVERAGE REPORT")
    print("=" * 50)

    print(f"Total Functions : {report['total']}")
    print(f"With Docstrings : {report['with_doc']}")
    print(f"Missing         : {report['missing']}")
    print(f"Coverage        : {report['coverage']}%")


if __name__ == "__main__":
    main()