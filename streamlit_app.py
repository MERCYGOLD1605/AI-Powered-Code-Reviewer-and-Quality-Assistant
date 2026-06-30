import streamlit as st
import os
import difflib

from ai.reviewer import generate_ai_docstring
from core.parser.python_parser import parse_file, get_source
from generator.docstring_generator import generate_docstring

from reports.coverage import generate_coverage_report
from core.quality_engine.quality_score import calculate_quality_score
from core.smell_engine.code_smells import detect_code_smells

if "results" not in st.session_state:
    st.session_state.results = []

st.title("AI Code Reviewer")

folder_path = st.text_input("Enter folder path:", "sample_code")

style = st.selectbox("Select Docstring Style", ["google", "numpy", "rest"])


search_term = st.text_input("Search function")
file_filter = st.text_input("Filter by file")


def insert_docstring(file_path, lineno, docstring):
    with open(file_path, "r") as f:
        lines = f.readlines()

    indent = " " * 4
    doc_lines = [indent + line + "\n" for line in docstring.split("\n")]

    lines.insert(lineno, "".join(doc_lines))

    with open(file_path, "w") as f:
        f.writelines(lines)

def preview_change(file_path, lineno, doc):
    with open(file_path, "r") as f:
        original = f.readlines()

    modified = original.copy()

    indent = " " * 4
    doc_lines = [indent + line + "\n" for line in doc.split("\n")]

    modified.insert(lineno, "".join(doc_lines))

    return "".join(original), "".join(modified)


def get_diff(original, modified):
    return "\n".join(difflib.unified_diff(
        original.splitlines(),
        modified.splitlines(),
        lineterm=""
    ))        
if st.button("Scan Code"):

    st.write("🚀 Scan Started")

    results = []
    all_functions = []

    for root, _, files in os.walk(folder_path):

        st.write(f"📁 Folder: {root}")

        for file in files:

            if file.endswith(".py"):

                st.write(f"📄 Scanning: {file}")

                file_path = os.path.join(root, file)

                functions = parse_file(file_path)

                st.write(f"Functions Found: {len(functions)}")

                all_functions.extend(functions)

                for func in functions:

                    st.write(f"Function: {func['name']}")

                    if func["docstring"] is None:

                        st.write(f"⚠ Missing Docstring: {func['name']}")

                        code_snippet = get_source(file_path, func["node"])

                        doc = generate_ai_docstring(code_snippet)

                        results.append({
                            "file": file,
                            "path": file_path,
                            "function": func["name"],
                            "lineno": func["lineno"],
                            "doc": doc
                        })

    st.write(f"✅ Total Functions Found: {len(all_functions)}")
    st.write(f"✅ Missing Docstrings: {len(results)}")

    st.session_state.coverage_report = generate_coverage_report(
        all_functions
    )

    st.session_state.quality_report = calculate_quality_score(
        all_functions
    )

    st.session_state.smells = detect_code_smells(
        all_functions
    )

if (
    "quality_report" in st.session_state
    and "coverage_report" in st.session_state
):

    st.subheader("📊 Project Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Functions",
        st.session_state.coverage_report["total"]
    )

    col2.metric(
        "Coverage",
        f"{st.session_state.coverage_report['coverage']}%"
    )

    col3.metric(
        "Quality Score",
        st.session_state.quality_report["overall"]
    )

    col4.metric(
        "Code Smells",
        len(st.session_state.smells)
    )

    st.divider()

if "results" in st.session_state:

    for i, res in enumerate(st.session_state.results):

        # ✅ FILTER
        if search_term and search_term.lower() not in res["function"].lower():
            continue

        if file_filter and file_filter.lower() not in res["file"].lower():
            continue

        st.subheader(f"{res['file']} → {res['function']}")

        # ✅ DIFF
        original, modified = preview_change(res["path"], res["lineno"], res["doc"])
        diff = get_diff(original, modified)

        st.code(diff, language="diff")

        col1, col2 = st.columns(2)

        # ✅ ACCEPT
        if col1.button(f"Accept {i}"):
            with open(res["path"], "w") as f:
                f.write(modified)

            st.success(f"Inserted docstring for {res['function']}")

        # ❌ REJECT
        if col2.button(f"Reject {i}"):
            st.warning(f"Skipped {res['function']}")