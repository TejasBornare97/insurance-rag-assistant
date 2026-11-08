"""
Generate the synthetic insurance policy PDFs and the answer key.

Run from the project folder:
    python -m scripts.generate_documents
"""

import json

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from scripts.policy_content import ANSWER_KEY, DOCUMENTS
from src.config import DOCUMENTS_DIR, ROOT_DIR

BRAND_COLOURS = {
    "Northgate Insurance": colors.HexColor("#1F4E79"),
    "Harbourline Insurance": colors.HexColor("#2E6B4F"),
}

# ---------------------------------------------------------------------------
# Text styles
# ---------------------------------------------------------------------------
BODY = ParagraphStyle("Body", fontName="Helvetica", fontSize=10, leading=14, spaceAfter=6)
SECTION = ParagraphStyle("Section", fontName="Helvetica-Bold", fontSize=13, leading=17,
                         spaceBefore=12, spaceAfter=6)
CLAUSE_TITLE = ParagraphStyle("ClauseTitle", fontName="Helvetica-Bold", fontSize=10,
                              leading=14, spaceBefore=4, spaceAfter=2)
TABLE_TEXT = ParagraphStyle("TableText", fontName="Helvetica", fontSize=9, leading=12)
TABLE_HEAD = ParagraphStyle("TableHead", fontName="Helvetica-Bold", fontSize=9, leading=12,
                            textColor=colors.white)


def make_canvas_class(doc_meta):
    """Create a canvas that draws a header and a 'Page X of Y' footer on every page.

    reportlab only knows the total page count at the very end, so we save each
    page and draw the footers when the document is finished.
    """
    brand = BRAND_COLOURS[doc_meta["insurer"]]

    class NumberedCanvas(canvas.Canvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._saved_pages = []

        def showPage(self):
            self._saved_pages.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            total = len(self._saved_pages)
            for state in self._saved_pages:
                self.__dict__.update(state)
                self._draw_header_footer(total)
                super().showPage()
            super().save()

        def _draw_header_footer(self, total):
            width, height = A4
            page = self._pageNumber

            # Header (not on the cover page)
            if page > 1:
                self.setFillColor(brand)
                self.setFont("Helvetica-Bold", 9)
                self.drawString(20 * mm, height - 12 * mm, doc_meta["insurer"])
                self.setFont("Helvetica", 9)
                self.drawRightString(width - 20 * mm, height - 12 * mm, doc_meta["title"])
                self.setStrokeColor(brand)
                self.line(20 * mm, height - 14 * mm, width - 20 * mm, height - 14 * mm)

            # Footer (every page)
            self.setFillColor(colors.grey)
            self.setFont("Helvetica", 8)
            self.drawString(20 * mm, 10 * mm,
                            f"Ref {doc_meta['reference']} | Effective {doc_meta['effective_date']}")
            self.drawRightString(width - 20 * mm, 10 * mm, f"Page {page} of {total}")
            self.drawCentredString(width / 2, 6 * mm,
                                   "Fictional document created for a software demonstration. "
                                   "Not a real insurance product.")

    return NumberedCanvas


def cover_page(doc):
    """Title page with insurer, title, reference and a contents list."""
    brand = BRAND_COLOURS[doc["insurer"]]
    title_style = ParagraphStyle("Title", fontName="Helvetica-Bold", fontSize=22, leading=28,
                                 textColor=brand, spaceAfter=10)
    insurer_style = ParagraphStyle("Insurer", fontName="Helvetica-Bold", fontSize=14,
                                   textColor=brand, spaceAfter=30)

    items = [
        Spacer(1, 30 * mm),
        Paragraph(doc["insurer"], insurer_style),
        Paragraph(doc["title"], title_style),
        Paragraph(f"Document type: {doc['doc_type']} | Product: {doc['product']}", BODY),
        Paragraph(f"Reference: {doc['reference']} | Effective from {doc['effective_date']}", BODY),
        Spacer(1, 10 * mm),
        Paragraph(doc["intro"], BODY),
        Spacer(1, 10 * mm),
        Paragraph("Contents", SECTION),
    ]
    for section in doc["sections"]:
        items.append(Paragraph(f"{section['number']}. {section['heading']}", BODY))
    items.append(PageBreak())
    return items


def make_table(rows, brand):
    """Turn a list of rows into a styled table. The first row is the header."""
    header, *body = rows
    data = [[Paragraph(cell, TABLE_HEAD) for cell in header]]
    data += [[Paragraph(cell, TABLE_TEXT) for cell in row] for row in body]

    usable_width = A4[0] - 40 * mm
    col_width = usable_width / len(header)
    table = Table(data, colWidths=[col_width] * len(header), repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), brand),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F5F7")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def section_flowables(section, brand):
    """Convert one section's blocks into reportlab flowables."""
    items = [Paragraph(f"{section['number']}. {section['heading']}", SECTION)]

    for block in section["blocks"]:
        kind = block[0]
        if kind == "p":
            items.append(Paragraph(block[1], BODY))
        elif kind == "clause":
            _, number, title, text = block
            items.append(Paragraph(f"{number} {title}", CLAUSE_TITLE))
            items.append(Paragraph(text, BODY))
        elif kind == "bullets":
            bullets = [ListItem(Paragraph(text, BODY), leftIndent=12) for text in block[1]]
            items.append(ListFlowable(bullets, bulletType="bullet", start="•", leftIndent=12))
        elif kind == "table":
            items.append(make_table(block[1], brand))
            items.append(Spacer(1, 6))
        else:
            raise ValueError(f"Unknown block type: {kind}")

    return items


def build_pdf(doc):
    """Build one PDF from a document dictionary."""
    path = DOCUMENTS_DIR / doc["filename"]
    brand = BRAND_COLOURS[doc["insurer"]]

    pdf = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=22 * mm, bottomMargin=20 * mm,
        title=doc["title"],
        author=doc["insurer"],
    )

    story = cover_page(doc)
    for section in doc["sections"]:
        story.extend(section_flowables(section, brand))

    pdf.build(story, canvasmaker=make_canvas_class(doc))
    return path


def main():
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    for doc in DOCUMENTS:
        path = build_pdf(doc)
        print(f"Created {path.name}")

    # Manifest: metadata about every document, used later for citations
    manifest = [
        {key: doc[key] for key in
         ("doc_id", "filename", "insurer", "product", "doc_type", "title", "reference", "effective_date")}
        for doc in DOCUMENTS
    ]
    manifest_path = ROOT_DIR / "data" / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Created {manifest_path.name}")

    answer_key_path = ROOT_DIR / "data" / "answer_key.json"
    answer_key_path.write_text(json.dumps(ANSWER_KEY, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Created {answer_key_path.name} ({len(ANSWER_KEY)} questions)")


if __name__ == "__main__":
    main()