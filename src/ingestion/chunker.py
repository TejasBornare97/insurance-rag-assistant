"""
Split parsed sections into chunks ready for embedding.

Rules:
  1. Never mix two sections or two documents in one chunk.
  2. Split on line boundaries, so a table row is never cut in half.
  3. Overlap neighbouring chunks slightly, so a sentence near a split
     still appears with its context.
  4. Start every chunk with a short header saying which insurer, product,
     document and section it came from.

Run from the project folder:
    python -m src.ingestion.chunker
"""

import json
import re
import statistics

from src.config import CHUNK_OVERLAP, CHUNK_SIZE, ROOT_DIR

INPUT_PATH = ROOT_DIR / "data" / "processed" / "parsed_sections.jsonl"
OUTPUT_PATH = ROOT_DIR / "data" / "processed" / "chunks.jsonl"

CONTENTS_LINE = re.compile(r"^\d+\.\s")          # e.g. "7. Excesses"
SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def load_records():
    with INPUT_PATH.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def is_contents_list(record):
    """The contents list on the cover page is just headings. It adds noise to search."""
    lines = record["text"].split("\n")
    return record["section"] == "0" and all(CONTENTS_LINE.match(line) for line in lines)


def make_header(record):
    """A short label that tells the search engine (and the LLM) where this text came from."""
    section = "Cover page" if record["section"] == "0" else f"Section {record['section']}: {record['heading']}"
    return f"{record['insurer']} | {record['product']} | {record['doc_type']} | {section}"


def split_into_pieces(text):
    """Break text into lines. Very long lines are broken further into sentences."""
    pieces = []
    for line in text.split("\n"):
        if len(line) <= CHUNK_SIZE:
            pieces.append(line)
        else:
            pieces.extend(SENTENCE_END.split(line))
    return pieces


def overlap_tail(lines):
    """The last few lines of a chunk, up to CHUNK_OVERLAP characters, to repeat in the next one."""
    tail = []
    for line in reversed(lines):
        if len("\n".join([line] + tail)) > CHUNK_OVERLAP:
            break
        tail.insert(0, line)
    return tail


def split_text(text):
    """Group pieces into chunks of up to CHUNK_SIZE characters, with overlap."""
    chunks, current = [], []

    for piece in split_into_pieces(text):
        if current and len("\n".join(current + [piece])) > CHUNK_SIZE:
            chunks.append("\n".join(current))
            current = overlap_tail(current)
        current.append(piece)

    if current:
        chunks.append("\n".join(current))
    return chunks


def chunk_record(record):
    """Turn one parsed section into one or more chunk dictionaries."""
    header = make_header(record)
    chunks = []

    for number, body in enumerate(split_text(record["text"]), start=1):
        chunks.append({
            "chunk_id": f"{record['doc_id']}-p{record['page']}-s{record['section']}-{number}",
            "text": f"{header}\n{body}",        # what we embed and show the LLM
            "doc_id": record["doc_id"],
            "insurer": record["insurer"],
            "product": record["product"],
            "doc_type": record["doc_type"],
            "title": record["title"],
            "page": record["page"],
            "section": record["section"],
            "heading": record["heading"],
        })
    return chunks


def main():
    records = load_records()
    kept = [r for r in records if not is_contents_list(r)]

    chunks = []
    for record in kept:
        chunks.extend(chunk_record(record))

    # Two records from the same page and section get the same id: make every id unique
    seen = {}
    for chunk in chunks:
        base = chunk["chunk_id"]
        seen[base] = seen.get(base, 0) + 1
        if seen[base] > 1:
            chunk["chunk_id"] = f"{base}-{seen[base]}"

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    sizes = [len(c["text"]) for c in chunks]
    print(f"Records in:        {len(records)} ({len(records) - len(kept)} contents lists skipped)")
    print(f"Chunks out:        {len(chunks)}")
    print(f"Chunk size (chars): min {min(sizes)}, median {int(statistics.median(sizes))}, max {max(sizes)}")
    print(f"Saved to {OUTPUT_PATH.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
