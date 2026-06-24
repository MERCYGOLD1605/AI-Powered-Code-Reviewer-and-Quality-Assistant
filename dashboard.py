import streamlit as st
from core.review_engine.ai_review import review_file

st.title("AI Code Reviewer")

file_path = st.text_input("Enter file path", "examples/sample_a.py")

if st.button("Review"):
    results = review_file(file_path)

    for r in results:
        st.subheader(r["function"])
        st.code(r["doc"], language="python")