from core.review_engine.ai_review import review_file

results = review_file("examples/sample_a.py")

for r in results:
    print(r["function"])
    print(r["doc"])