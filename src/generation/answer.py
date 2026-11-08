"""
Answer a question using only the retrieved policy text, with citations.

Run from the project folder:
    python -m src.generation.answer "What is the Harbourline escape of water excess?"
or with no question to run a few examples.
"""

import re
import sys

from src.config import TOP_K
from src.generation.llm import generate
from src.retrieval.retriever import retrieve

NOT_FOUND = "I can't find this in the policy documents provided."

SYSTEM_PROMPT = f"""You are an assistant for insurance staff. You answer questions about policy documents.

Rules:
1. Use ONLY the numbered sources provided. Never use outside knowledge.
2. After every fact, cite the SOURCE number in square brackets, e.g. [2]. Use the number before the source's title, not a clause or section number from inside the text. Cite every source you use.
3. Quote amounts, limits and time periods exactly as written in the source.
4. Different insurers have different terms. Always say which insurer and product a fact applies to. Never apply one insurer's terms to another.
5. If the question does not name an insurer and the sources show different answers for different insurers, give each insurer's answer separately.
6. If a source answers the question with a rule, formula or condition instead of a single figure (for example "X% of the sum insured or £Y, whichever is lower"), state that rule. That is a valid answer.
7. Never make a cover decision the sources do not state. If the sources clearly answer the question, just answer it: do not add a referral. Only if the sources do not specifically mention what the question asks about, say so, give the closest relevant clause with its citation, and say the question should be referred for a decision. Do not conclude "covered" or "not covered" yourself.
8. Only if NONE of the sources is relevant to the question, reply exactly: "{NOT_FOUND}"
9. Be concise: a direct answer in 1 to 4 sentences, in plain UK English."""


def format_source(number, hit):
    """Label a chunk so the model and the reader know exactly where it came from."""
    return (f"[{number}] {hit['insurer']} - {hit['title']}, page {hit['page']}, "
            f"section {hit['section']} ({hit['heading']})\n{hit['text']}")


def build_prompt(question, hits):
    sources = "\n\n".join(format_source(n, hit) for n, hit in enumerate(hits, start=1))
    return f"Sources:\n\n{sources}\n\nQuestion: {question}\n\nAnswer (with citations):"


def cited_numbers(answer):
    """Source numbers cited in the answer.

    Models don't always cite neatly, so we accept:
      [2]       source 2
      [1, 3]    sources 1 and 3
      [1.2]     source 1 (the model added the clause number, 1.2, to the source number)
    """
    numbers = set()
    for group in re.findall(r"\[([\d.,\s]+)\]", answer):
        for part in group.split(","):
            part = part.strip()
            if part:
                numbers.add(int(part.split(".")[0]))
    return sorted(numbers)


def extract_citations(answer, hits):
    """Match the cited numbers to the sources. Numbers that match no real source are ignored."""
    return [{"number": n, **hits[n - 1]} for n in cited_numbers(answer) if 1 <= n <= len(hits)]


def answer_question(question, top_k=TOP_K, mode="hybrid", auto_filter=True):
    """The full RAG pipeline: retrieve, build the prompt, generate, attach citations."""
    hits = retrieve(question, top_k=top_k, mode=mode, auto_filter=auto_filter)
    if not hits:
        return {"question": question, "answer": NOT_FOUND, "citations": [], "sources": [],
                "status": "not_found", "unsupported_figures": []}

    answer = generate(SYSTEM_PROMPT, build_prompt(question, hits))
    citations = extract_citations(answer, hits)
    unsupported = unsupported_figures(answer, citations)

    if NOT_FOUND.lower().rstrip(".") in answer.lower():
        status = "not_found"
    elif unsupported:
        status = "unsupported_figures"   # a figure not found in the cited sources: likely invented
    elif not citations:
        status = "uncited"               # an answer with no citations can't be checked
    elif "refer" in answer.lower():
        status = "referral"              # the documents don't settle it: a person should decide
    else:
        status = "answered"

    return {"question": question, "answer": answer, "citations": citations, "sources": hits,
            "status": status, "unsupported_figures": unsupported}


def unsupported_figures(answer, citations):
    """Grounding check: every £ amount and percentage in the answer must appear in a cited source.

    We don't rely on the model to police itself. If it writes a figure that isn't
    in the text it cited, the figure was misread or invented.
    """
    figures = set(re.findall(r"£\d[\d,]*(?:\.\d+)?|\d+(?:\.\d+)?%", answer))
    cited_text = " ".join(c["text"] for c in citations)
    return sorted(f for f in figures if f not in cited_text)


def print_result(result):
    print(f"\nQ: {result['question']}")
    print(f"A: {result['answer']}")
    if result["status"] == "uncited":
        print("   WARNING: the answer has no citations, so it can't be verified.")
    if result["status"] == "unsupported_figures":
        print(f"   WARNING: these figures are not in the cited sources: {', '.join(result['unsupported_figures'])}")
    if result["citations"]:
        print("Sources:")
        for c in result["citations"]:
            print(f"  [{c['number']}] {c['insurer']} - {c['title']}, page {c['page']}, "
                  f"section {c['section']} ({c['heading']})")
    elif result["sources"]:
        # Nothing cited: show what was retrieved, to tell a retrieval miss from a model miss
        print("Retrieved but not used:")
        for n, s in enumerate(result["sources"], start=1):
            print(f"  [{n}] {s['insurer']} - {s['title']}, page {s['page']}, "
                  f"section {s['section']} ({s['heading']})")


EXAMPLES = [
    "What is the escape of water excess?",                      # no insurer named: should give both
    "Is my Northgate car covered for theft if I left the keys in it?",
    "Who can authorise a claim worth £30,000?",
    "How much will Harbourline pay for alternative accommodation?",  # answer is a rule, not a figure
    "Does Northgate home insurance cover damage caused by a drone?",   # grey area: should refer, not decide
    "What is the Harbourline travel insurance baggage limit?",          # no such document: must refuse
]

if __name__ == "__main__":
    questions = [" ".join(sys.argv[1:])] if len(sys.argv) > 1 else EXAMPLES
    for q in questions:
        print_result(answer_question(q))
