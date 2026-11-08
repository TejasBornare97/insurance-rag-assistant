"""
Measure how well each search approach finds the right section.

For every question in the answer key that has a known source, we check
whether the correct document AND section appear in the top results.

Run from the project folder:
    python -m scripts.evaluate_retrieval
"""

import json
from collections import defaultdict

from src.config import ROOT_DIR
from src.retrieval.retriever import detect_filters, retrieve

ANSWER_KEY_PATH = ROOT_DIR / "data" / "answer_key.json"
TOP_K = 5

SETUPS = [
    ("Vector only", {"mode": "vector", "auto_filter": False}),
    ("Keyword only", {"mode": "keyword", "auto_filter": False}),
    ("Hybrid", {"mode": "hybrid", "auto_filter": False}),
    ("Hybrid + filters", {"mode": "hybrid", "auto_filter": True}),
]


def load_questions():
    questions = json.loads(ANSWER_KEY_PATH.read_text(encoding="utf-8"))
    return [q for q in questions if q["doc_id"]]   # skip questions with no answer in the documents


def rank_of_correct(question, hits):
    """Position (1, 2, 3...) of the first correct chunk, or None if it is missing."""
    for rank, hit in enumerate(hits, start=1):
        if hit["doc_id"] == question["doc_id"] and hit["section"] == question["section"]:
            return rank
    return None


def evaluate(settings, questions):
    results = []
    for q in questions:
        hits = retrieve(q["question"], top_k=TOP_K, **settings)
        results.append({"question": q, "rank": rank_of_correct(q, hits), "top_hit": hits[0] if hits else None})
    return results


def summarise(results):
    n = len(results)
    hit_1 = sum(r["rank"] == 1 for r in results) / n
    hit_k = sum(r["rank"] is not None for r in results) / n
    mrr = sum(1 / r["rank"] for r in results if r["rank"]) / n
    return hit_1, hit_k, mrr


def main():
    questions = load_questions()
    print(f"Evaluating {len(questions)} questions, top {TOP_K} results each\n")

    print(f"{'Setup':20} {'Hit@1':>7} {'Hit@5':>7} {'MRR':>6}")
    print("-" * 43)
    all_results = {}
    for name, settings in SETUPS:
        results = evaluate(settings, questions)
        all_results[name] = results
        hit_1, hit_k, mrr = summarise(results)
        print(f"{name:20} {hit_1:7.0%} {hit_k:7.0%} {mrr:6.2f}")

    best = all_results["Hybrid + filters"]

    print("\nHybrid + filters, by question type:")
    by_type = defaultdict(list)
    for r in best:
        by_type[r["question"]["type"]].append(r)
    for qtype, rows in sorted(by_type.items()):
        found = sum(r["rank"] is not None for r in rows)
        print(f"  {qtype:14} {found}/{len(rows)} found in top {TOP_K}")

    misses = [r for r in best if r["rank"] != 1]
    if misses:
        print("\nNot ranked first (Hybrid + filters):")
        for r in misses:
            q = r["question"]
            top = r["top_hit"]
            where = f"rank {r['rank']}" if r["rank"] else "not in top 5"
            print(f"  {q['id']} [{where}] {q['question']}")
            print(f"      expected {q['doc_id']} s{q['section']} | got {top['doc_id']} s{top['section']}"
                  f" | filters {detect_filters(q['question']) or 'none'}")


if __name__ == "__main__":
    main()
