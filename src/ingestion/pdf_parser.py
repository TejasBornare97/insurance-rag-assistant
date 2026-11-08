"""
Turn policy PDFs into clean, structured text.

For every document we produce one record per (page, section) with:
    doc_id, insurer, product, doc_type, title, page, section, heading, text

Run from the project folder:
    python -m src.ingestion.pdf_parser
"""

import json
import re

import pymupdf

from src.config import DOCUMENTS_DIR, ROOT_DIR

MANIFEST_PATH = ROOT_DIR / "data" / "manifest.json"
OUTPUT_PATH = ROOT_DIR / "data" / "processed" / "parsed_sections.jsonl"

# Header sits in the top ~16mm of each page and the footer in the bottom ~18mm.
# 1mm is about 2.83 points, the unit PDFs use for positions.
HEADER_HEIGHT = 45
FOOTER_HEIGHT = 50

SECTION_HEADING_SIZE = 12.5   # section headings are 13pt bold; body text is 10pt
SAME_ROW_TOLERANCE = 2        # blocks whose tops are within 2pt are in the same row
COLUMN_TOLERANCE = 8          # lines starting within ~8pt of each other are in the same column
SECTION_PATTERN = re.compile(r"^(\d+)\.\s+(.+)$")


def load_manifest():
    """Read the metadata we saved for every document."""
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def block_text(block):
    """Join the lines of a text block into one string.

    Lines that start at the same left position belong to the same column.
    A normal paragraph has one column. A table row has one column per cell,
    so we join cells with ' | ' to keep each value next to its label.
    """
    columns = {}
    for line in block["lines"]:
        text = "".join(span["text"] for span in line["spans"]).strip()
        if not text:
            continue
        # Where the words start. Skip a leading bullet symbol, otherwise the first
        # line of a bullet looks like a different column from its wrapped lines.
        word_spans = [s for s in line["spans"] if s["text"].strip() not in ("", "•")]
        start_x = word_spans[0]["bbox"][0] if word_spans else line["bbox"][0]

        x = round(start_x / COLUMN_TOLERANCE)   # lines starting close together = same column
        columns.setdefault(x, []).append(text)

    cells = [" ".join(columns[x]) for x in sorted(columns)]
    return " | ".join(cells).replace("•", "-")


def is_section_heading(block):
    """A section heading is large bold text, e.g. '7. Excesses'."""
    first_span = block["lines"][0]["spans"][0]
    return first_span["size"] >= SECTION_HEADING_SIZE and "Bold" in first_span["font"]


def group_into_rows(blocks):
    """Group blocks that sit side by side on the same line.

    A normal paragraph is a single block on its own row. A table row is
    several blocks (one per cell) that share the same top edge.
    """
    blocks = sorted(blocks, key=lambda b: (round(b["bbox"][1]), b["bbox"][0]))
    rows = []
    for block in blocks:
        if rows and abs(block["bbox"][1] - rows[-1][0]["bbox"][1]) <= SAME_ROW_TOLERANCE:
            rows[-1].append(block)
        else:
            rows.append([block])
    # Within a row, read cells left to right
    return [sorted(row, key=lambda b: b["bbox"][0]) for row in rows]


def row_to_text(row):
    """Turn a row into text. Table rows become 'cell | cell | cell'."""
    cells = [block_text(block) for block in row]
    return " | ".join(cell for cell in cells if cell)


def parse_document(doc_meta):
    """Parse one PDF into a list of (page, section) records."""
    pdf = pymupdf.open(DOCUMENTS_DIR / doc_meta["filename"])

    records = []
    section, heading = "0", "Cover and contents"
    buffer = []

    def save_buffer(page_number):
        text = "\n".join(buffer).strip()
        if text:
            records.append({
                "doc_id": doc_meta["doc_id"],
                "insurer": doc_meta["insurer"],
                "product": doc_meta["product"],
                "doc_type": doc_meta["doc_type"],
                "title": doc_meta["title"],
                "page": page_number,
                "section": section,
                "heading": heading,
                "text": text,
            })
        buffer.clear()

    for page_number, page in enumerate(pdf, start=1):
        # Only read the body of the page: skip the header and footer areas
        body_area = pymupdf.Rect(0, HEADER_HEIGHT, page.rect.width, page.rect.height - FOOTER_HEIGHT)
        blocks = [b for b in page.get_text("dict", clip=body_area)["blocks"] if b["type"] == 0]

        for row in group_into_rows(blocks):
            if len(row) == 1 and is_section_heading(row[0]):
                save_buffer(page_number)
                match = SECTION_PATTERN.match(block_text(row[0]))
                if match:
                    section, heading = match.group(1), match.group(2)
                continue
            buffer.append(row_to_text(row))

        save_buffer(page_number)   # a page boundary always starts a new record

    return records


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    all_records = []

    for doc_meta in load_manifest():
        records = parse_document(doc_meta)
        all_records.extend(records)
        print(f"{doc_meta['doc_id']:30} {len(records):3} sections")

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        for record in all_records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"\nSaved {len(all_records)} records to {OUTPUT_PATH.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
