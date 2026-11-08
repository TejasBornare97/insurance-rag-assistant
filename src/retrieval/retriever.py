"""
Find the chunks that best answer a question.

Combines two kinds of search:
  - vector search (meaning):   finds "escape of water" when asked about a "burst pipe"
  - keyword search (BM25):     rewards exact words like "excess", "£30,000", "Harbourline"
and merges their rankings with Reciprocal Rank Fusion.

It also spots insurer and product names in the question and filters the
search to matching documents automatically.
"""

import json
import re
from functools import lru_cache

from rank_bm25 import BM25Okapi

from src.config import ROOT_DIR, TOP_K
from src.retrieval.vector_store import search as vector_search

CHUNKS_PATH = ROOT_DIR / "data" / "processed" / "chunks.jsonl"

CANDIDATES = 20   # how many results each method contributes before merging
RRF_K = 60        # standard constant for Reciprocal Rank Fusion

# Words in a question that point to an insurer or product
INSURER_KEYWORDS = {
    "Northgate Insurance": ["northgate"],
    "Harbourline Insurance": ["harbourline"],
}
PRODUCT_KEYWORDS = {
    # "home" alone is too loose ("after returning home" is a travel question),
    # so Home is only matched on phrases or unambiguous words.
    "Home": ["home insurance", "home policy", "home contents", "house", "household",
             "buildings", "contents"],
    "Motor": ["car", "motor", "vehicle", "windscreen", "driver", "driving"],
    "Travel": ["travel", "trip", "holiday"],
}
SHARED_PRODUCT = "All products"   # the claims procedure applies to every product

STOPWORDS = {
    "a", "an", "the", "is", "are", "am", "i", "my", "me", "you", "your", "what", "which",
    "who", "how", "when", "does", "do", "can", "if", "of", "on", "in", "to", "for", "and",
    "or", "it", "be", "under", "with", "this", "that", "much", "many", "there",
}


# ---------------------------------------------------------------------------
# Automatic filters
# ---------------------------------------------------------------------------
def detect_filters(question):
    """Return {field: [allowed values]} based on names found in the question."""
    # Pad with spaces so " car " matches the word "car" but not "card" or "scarf"
    text = " " + " ".join(re.findall(r"[a-z]+", question.lower())) + " "

    def mentions(keywords):
        return any(f" {keyword} " in text for keyword in keywords)

    filters = {}

    insurers = [name for name, keys in INSURER_KEYWORDS.items() if mentions(keys)]
    if insurers:
        filters["insurer"] = insurers

    products = [name for name, keys in PRODUCT_KEYWORDS.items() if mentions(keys)]
    if products:
        filters["product"] = products + [SHARED_PRODUCT]

    return filters


def to_chroma_where(filters):
    """Convert our filter format into ChromaDB's 'where' syntax."""
    conditions = [{field: {"$in": values}} for field, values in filters.items()]
    if not conditions:
        return None
    if len(conditions) == 1:
        return conditions[0]
    return {"$and": conditions}


def matches(chunk, filters):
    """Check a chunk against our filters (used for keyword search)."""
    return all(chunk[field] in values for field, values in filters.items())


# ---------------------------------------------------------------------------
# Keyword search (BM25)
# ---------------------------------------------------------------------------
def tokenize(text):
    """Lowercase words and numbers, without very common words.

    '£30,000' becomes '30000' so it matches however it is written.
    """
    text = text.lower().replace(",", "")
    return [t for t in re.findall(r"[a-z]+|\d+", text) if t not in STOPWORDS]


@lru_cache(maxsize=1)
def load_keyword_index():
    """Read every chunk and build the BM25 keyword index once."""
    with CHUNKS_PATH.open(encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f]
    index = BM25Okapi([tokenize(c["text"]) for c in chunks])
    return chunks, index


def keyword_search(question, top_k, filters):
    chunks, index = load_keyword_index()
    scores = index.get_scores(tokenize(question))
    ranked = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)

    hits = []
    for i in ranked:
        if scores[i] <= 0:
            break
        if matches(chunks[i], filters):
            hits.append({**chunks[i], "score": round(float(scores[i]), 3)})
        if len(hits) == top_k:
            break
    return hits


# ---------------------------------------------------------------------------
# Combining the two: Reciprocal Rank Fusion
# ---------------------------------------------------------------------------
def reciprocal_rank_fusion(*result_lists):
    """Merge ranked lists. A chunk ranked highly by either method rises to the top.

    Each list gives a chunk 1 / (60 + rank) points. We use ranks rather than raw
    scores because vector scores (0 to 1) and BM25 scores (0 to 20+) are on
    completely different scales.
    """
    fused, chunk_by_id = {}, {}
    for results in result_lists:
        for rank, hit in enumerate(results, start=1):
            fused[hit["chunk_id"]] = fused.get(hit["chunk_id"], 0) + 1 / (RRF_K + rank)
            chunk_by_id.setdefault(hit["chunk_id"], hit)

    ordered = sorted(fused, key=fused.get, reverse=True)
    return [{**chunk_by_id[cid], "score": round(fused[cid], 4)} for cid in ordered]


# ---------------------------------------------------------------------------
# The one function the rest of the app calls
# ---------------------------------------------------------------------------
def retrieve(question, top_k=TOP_K, mode="hybrid", auto_filter=True):
    """Return the top_k most relevant chunks for a question.

    mode: "vector", "keyword" or "hybrid"
    auto_filter: narrow the search using insurer/product names in the question
    """
    filters = detect_filters(question) if auto_filter else {}
    where = to_chroma_where(filters)

    if mode == "vector":
        return vector_search(question, top_k=top_k, where=where)
    if mode == "keyword":
        return keyword_search(question, top_k, filters)

    vector_hits = vector_search(question, top_k=CANDIDATES, where=where)
    keyword_hits = keyword_search(question, CANDIDATES, filters)
    return reciprocal_rank_fusion(vector_hits, keyword_hits)[:top_k]


if __name__ == "__main__":
    question = "What is the excess for escape of water under Harbourline?"
    print(f"Q: {question}")
    print(f"Filters detected: {detect_filters(question)}\n")
    for mode in ("vector", "keyword", "hybrid"):
        print(f"[{mode}]")
        for rank, hit in enumerate(retrieve(question, top_k=3, mode=mode), start=1):
            print(f"  {rank}. {hit['doc_id']}  page {hit['page']}  section {hit['section']} ({hit['heading']})")
