"""
Store chunk embeddings in ChromaDB and search them.

Build (or rebuild) the database from chunks.jsonl:
    python -m src.retrieval.vector_store
"""

import json

import chromadb

from src.config import CHROMA_DIR, COLLECTION_NAME, ROOT_DIR, TOP_K
from src.retrieval.embedder import embed_query, embed_texts

CHUNKS_PATH = ROOT_DIR / "data" / "processed" / "chunks.jsonl"
METADATA_FIELDS = ("doc_id", "insurer", "product", "doc_type", "title", "page", "section", "heading")


def get_client():
    """A Chroma database saved on disk in the chroma_db folder."""
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_collection():
    """Open the collection (Chroma's word for a table) of policy chunks.

    embedding_function=None: we create embeddings ourselves with our own model,
    so Chroma never silently uses a different one.
    hnsw:space = cosine: measure closeness with cosine similarity, as in Step 5.
    """
    return get_client().get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=None,
        metadata={"hnsw:space": "cosine"},
    )


def load_chunks():
    with CHUNKS_PATH.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def build_index():
    """Embed every chunk and store it. Rebuilds from scratch each time."""
    client = get_client()
    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION_NAME)

    collection = get_collection()
    chunks = load_chunks()

    print(f"Embedding {len(chunks)} chunks...")
    embeddings = embed_texts([c["text"] for c in chunks], show_progress=True)

    collection.add(
        ids=[c["chunk_id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        embeddings=embeddings,
        metadatas=[{field: c[field] for field in METADATA_FIELDS} for c in chunks],
    )
    print(f"Stored {collection.count()} chunks in {CHROMA_DIR.name}/")
    return collection


def search(question, top_k=TOP_K, where=None):
    """Find the chunks closest in meaning to the question.

    where: optional metadata filter, e.g. {"insurer": "Harbourline Insurance"}.
    Returns a list of dicts with the text, its metadata and a similarity score
    (1 = identical meaning, 0 = unrelated).
    """
    results = get_collection().query(
        query_embeddings=[embed_query(question)],
        n_results=top_k,
        where=where,
    )

    hits = []
    for chunk_id, text, metadata, distance in zip(
        results["ids"][0], results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        hits.append({"chunk_id": chunk_id, "text": text, "score": round(1 - distance, 3), **metadata})
    return hits


def print_hits(question, hits):
    print(f"\nQ: {question}")
    for rank, hit in enumerate(hits, start=1):
        print(f"  {rank}. {hit['score']:.3f}  {hit['doc_id']}  page {hit['page']}  "
              f"section {hit['section']} ({hit['heading']})")


def main():
    build_index()

    question = "What is the excess for escape of water?"
    print_hits(question, search(question, top_k=3))

    # The same question, filtered to one insurer using metadata
    filtered = search(question, top_k=3, where={"insurer": "Harbourline Insurance"})
    print_hits(question + "  [filter: Harbourline only]", filtered)


if __name__ == "__main__":
    main()
