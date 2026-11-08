"""
A hands-on look at embeddings before we build the vector database.

Run from the project folder:
    python -m scripts.explore_embeddings
"""

import json

import numpy as np

from src.config import EMBEDDING_MODEL, ROOT_DIR
from src.retrieval.embedder import embed_query, embed_texts, get_model

CHUNKS_PATH = ROOT_DIR / "data" / "processed" / "chunks.jsonl"


def heading(text):
    print(f"\n{'=' * 70}\n{text}\n{'=' * 70}")


def part_1_what_an_embedding_looks_like():
    heading("PART 1: What does an embedding look like?")
    vector = embed_query("What is the excess for escape of water?")
    print(f"Model: {EMBEDDING_MODEL}")
    print(f"Max text length the model reads: {get_model().max_seq_length} tokens")
    print(f"The sentence became a list of {len(vector)} numbers.")
    print(f"First 8 numbers: {[round(x, 3) for x in vector[:8]]}")


def part_2_meaning_not_words():
    heading("PART 2: Similar meaning, different words")
    question = "My pipe burst and flooded the kitchen. Am I covered?"
    candidates = [
        "Escape of water: water escaping from any fixed water or heating installation.",
        "Theft or attempted theft of the car if the keys were left in it.",
        "Emergency medical expenses abroad up to £10,000,000.",
        "The pipe organ in the church is very old.",
    ]
    q = np.array(embed_query(question))
    c = np.array(embed_texts(candidates))
    scores = c @ q   # dot product of normalised vectors = cosine similarity

    print(f"Question: {question}\n")
    for score, text in sorted(zip(scores, candidates), reverse=True):
        print(f"  {score:.3f}  {text}")
    print("\nNotice: 'escape of water' wins without sharing the words 'pipe' or 'burst',")
    print("and the church sentence scores low even though it contains 'pipe'.")


def part_3_search_our_chunks():
    heading("PART 3: Search all our chunks (brute force)")
    with CHUNKS_PATH.open(encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f]

    print(f"Embedding {len(chunks)} chunks...")
    matrix = np.array(embed_texts([c["text"] for c in chunks], show_progress=True))
    print(f"Embedding matrix shape: {matrix.shape} (chunks x numbers per chunk)")

    questions = [
        "What is the Harbourline excess for a leak?",
        "Is my car covered for theft if I left the keys inside?",
        "Who can authorise a claim worth £30,000?",
    ]
    for question in questions:
        scores = matrix @ np.array(embed_query(question))
        top = np.argsort(scores)[::-1][:3]
        print(f"\nQ: {question}")
        for rank, i in enumerate(top, start=1):
            c = chunks[i]
            print(f"  {rank}. {scores[i]:.3f}  {c['doc_id']}  page {c['page']}  section {c['section']} ({c['heading']})")


if __name__ == "__main__":
    part_1_what_an_embedding_looks_like()
    part_2_meaning_not_words()
    part_3_search_our_chunks()
