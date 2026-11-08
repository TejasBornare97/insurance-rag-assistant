"""
Run every question in the answer key through the full system and score the answers.

What we measure, per question:
  correct      - the answer contains the key facts (figures, deadlines, roles)
  right_doc    - at least one citation points to the correct document
  right_sect   - at least one citation points to the correct document AND section
  safe         - no figures missing from the cited sources (no invented numbers)
For questions with no answer in the documents, "correct" means the system
refused or referred instead of answering.

Every answer is also saved to a CSV for a person to review, because automatic
checks are approximate.

Run from the project folder:
    python -m scripts.evaluate_answers               (all 29 questions, ~10-20 minutes)
    python -m scripts.evaluate_answers Q01 Q08 Q28   (just these)
"""

import csv
import json
import re
import sys
import time
from collections import defaultdict

from src.config import ROOT_DIR
from src.generation.answer import answer_question

ANSWER_KEY_PATH = ROOT_DIR / "data" / "answer_key.json"
REPORT_DIR = ROOT_DIR / "reports"
TOP_K = 4

# What a correct answer must contain. Each inner list is a group of acceptable
# alternatives: the answer must match at least one alternative from EVERY group.
NEGATIVE = ["not covered", "isn't covered", "is not covered", "won't be covered", "will not be covered",
            "not be covered", "won't cover", "will not cover", "does not cover", "doesn't cover", "excluded"]
EXPECTED_TERMS = {
    "Q01": [["250"]],
    "Q02": [["500"]],
    "Q03": [["5000"]],
    "Q04": [["500"]],
    "Q05": [["300"]],
    "Q06": [["31"]],
    "Q07": [["10000000", "10 million", "10m"]],
    "Q08": [["350"]],
    "Q09": [["400"]],
    "Q10": [["3000"]],
    "Q11": [["400"]],
    "Q12": [["30"]],
    "Q13": [["60", "61"]],
    "Q14": [NEGATIVE + ["^no"]],
    "Q15": [["25"], ["^no", "not", "cannot", "can't", "only applies"]],
    "Q16": [["^no", "not", "doesn't", "cannot", "can't", "only covered", "only the car"]],
    "Q17": [NEGATIVE + ["^no", "not covered at all", "no cover"]],
    "Q18": [["^no", "not affect", "doesn't affect", "won't affect", "will not affect", "no effect"]],
    "Q19": [["30"]],
    "Q20": [["48"]],
    "Q21": [["48"]],
    "Q22": [["31"]],
    "Q23": [["senior"]],
    "Q24": [["subsidence"], ["7500"], ["15000"]],
    "Q25": [["1 working day", "one working day"]],
    "Q26": [["senior"]],
    "Q27": [["550"]],
}
SAFE_STATUSES_FOR_UNANSWERABLE = {"not_found", "referral"}


def normalise(text):
    """Lowercase, drop commas and £ signs, so '£5,000' matches '5000'."""
    return text.lower().replace(",", "").replace("£", "")


def contains(text, term):
    """Check one expected term.

    Numbers must match as whole numbers: '30' should not match '300'.
    A term starting with ^ must come at the start of the answer: '^no' accepts
    "No, ..." without matching the "no" in "no claims discount".
    """
    if term.startswith("^"):
        return re.match(rf"\W*{re.escape(term[1:])}\b", text) is not None
    if term.isdigit():
        return re.search(rf"(?<!\d){term}(?!\d)", text) is not None
    return term in text


def has_expected_facts(question_id, answer):
    text = normalise(answer)
    return all(any(contains(text, alt) for alt in group) for group in EXPECTED_TERMS[question_id])


def score(q, result):
    answerable = q["doc_id"] is not None
    cited = [(c["doc_id"], c["section"]) for c in result["citations"]]

    if answerable:
        correct = has_expected_facts(q["id"], result["answer"])
        right_doc = any(doc == q["doc_id"] for doc, _ in cited)
        right_sect = (q["doc_id"], q["section"]) in cited
    else:
        correct = result["status"] in SAFE_STATUSES_FOR_UNANSWERABLE
        right_doc = right_sect = None

    return {
        "id": q["id"], "type": q["type"], "question": q["question"],
        "expected": q["answer"], "answer": result["answer"], "status": result["status"],
        "correct": correct, "right_doc": right_doc, "right_sect": right_sect,
        "safe": not result["unsupported_figures"],
        "unsupported_figures": ", ".join(result["unsupported_figures"]),
        "citations": "; ".join(f"{d} s{s}" for d, s in cited),
    }


def rate(rows, field):
    values = [r[field] for r in rows if r[field] is not None]
    return f"{sum(values)}/{len(values)}" if values else "-"


def main():
    questions = json.loads(ANSWER_KEY_PATH.read_text(encoding="utf-8"))
    wanted = set(sys.argv[1:])
    if wanted:
        questions = [q for q in questions if q["id"] in wanted]

    rows = []
    for n, q in enumerate(questions, start=1):
        start = time.time()
        result = answer_question(q["question"], top_k=TOP_K)
        row = score(q, result)
        row["seconds"] = round(time.time() - start, 1)
        rows.append(row)
        mark = "PASS" if row["correct"] else "FAIL"
        print(f"[{n}/{len(questions)}] {q['id']} {mark:4} {row['status']:20} {row['seconds']:5.1f}s  {q['question'][:60]}")

    # Save every answer for human review
    REPORT_DIR.mkdir(exist_ok=True)
    csv_path = REPORT_DIR / "answer_evaluation.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    answerable = [r for r in rows if r["right_doc"] is not None]
    unanswerable = [r for r in rows if r["right_doc"] is None]

    print("\n" + "=" * 50)
    print("RESULTS")
    print("=" * 50)
    print(f"Correct answers (answerable):     {rate(answerable, 'correct')}")
    print(f"Cited the right document:         {rate(answerable, 'right_doc')}")
    print(f"Cited the right section:          {rate(answerable, 'right_sect')}")
    print(f"Refused/referred when no answer:  {rate(unanswerable, 'correct')}")
    print(f"No invented figures:              {rate(rows, 'safe')}")
    print(f"Average time per answer:          {sum(r['seconds'] for r in rows) / len(rows):.1f}s")

    print("\nBy question type (correct):")
    by_type = defaultdict(list)
    for r in rows:
        by_type[r["type"]].append(r)
    for qtype, group in sorted(by_type.items()):
        print(f"  {qtype:14} {rate(group, 'correct')}")

    failures = [r for r in rows if not r["correct"] or not r["safe"]]
    if failures:
        print("\nTo review:")
        for r in failures:
            problem = "wrong/incomplete" if not r["correct"] else f"unsupported figures {r['unsupported_figures']}"
            print(f"  {r['id']} ({problem}): {r['question']}")
            print(f"      expected: {r['expected']}")
            print(f"      got:      {r['answer'][:160].replace(chr(10), ' ')}")

    print(f"\nFull answers saved to {csv_path.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
