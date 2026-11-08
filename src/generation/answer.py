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
2. After every fact, cite its source number in square brackets, e.g. [2]. Cite every source you use.
3. Quote amounts, limits and time periods exactly as written in the source.
4. Different insurers have different terms. Always say which insurer and product a fact applies to. Never apply one insurer's terms to another.
5. If the question does not name an insurer and the sources show different answers for different insurers, give each insurer's answer separately.
6. If a source answers the question with a rule, formula or condition instead of a single figure (for example "X% of the sum insured or £Y, whichever is lower"), state that rule. That is a valid answer.
7. Never make a cover decision the sources do not state. If the sources do not specifically mention what the question asks about, say so, give the closest relevant clause with its citation, and say the question should be referred for a decision. Do not conclude "covered" or "not covered" yourself.
8. Only if NONE of the sources is relevant to the question, reply exactly: "{NOT_FOUND}"
9. Be concise: a direct answer in 1 to 4 sentences, in plain UK English."""


def format_source(number, hit):
    """Label a chunk so the model and the reader know exactly where it came from."""
    return (f"[{number}] {hit['insurer']} - {hit['title']}, page {hit['page']}, "
            f"section {hit['section']} ({hit['heading']})\n{hit['text']}")


def build_prompt(question, hits):
    sources = "\n\n".join(format_source(n, hit) for n, hit in enumerate(hits, start=1))
    return f"Sources:\n\n{sources}\n\nQuestion: {question}\n\nAnswer (with citations):"


def extract_citations(answer, hits):
    """Find the [n] markers in the answer and match them to the sources.

    Numbers the model invents that don't match a real source are ignored.
    """
    numbers = sorted({int(n) for n in re.findall(r"\[(\d+)\]", answer)})
    return [{"number": n, **hits[n - 1]} for n in numbers if 1 <= n <= len(hits)]


def answer_question(question, top_k=TOP_K):
    """The full RAG pipeline: retrieve, build the prompt, generate, attach citations."""
    hits = retrieve(question, top_k=top_k)
    if not hits:
        return {"question": question, "answer": NOT_FOUND, "citations": [], "sources": [], "status": "not_found"}

    answer = generate(SYSTEM_PROMPT, build_prompt(question, hits))
    citations = extract_citations(answer, hits)

    if NOT_FOUND.lower().rstrip(".") in answer.lower():
        status = "not_found"
    elif citations:
        status = "answered"
    else:
        status = "uncited"   # an answer with no citations can't be checked: treat with caution

    return {"question": question, "answer": answer, "citations": citations, "sources": hits, "status": status}


def print_result(result):
    print(f"\nQ: {result['question']}")
    print(f"A: {result['answer']}")
    if result["status"] == "uncited":
        print("   WARNING: the answer has no citations, so it can't be verified.")
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
