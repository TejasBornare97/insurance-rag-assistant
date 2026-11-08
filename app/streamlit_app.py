"""
AI Document Assistant - web interface.

Run from the project folder:
    streamlit run app/streamlit_app.py
"""

import sys
from pathlib import Path

# Streamlit runs this file from the app/ folder; make the project folder importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pymupdf
import streamlit as st

from src.config import DOCUMENTS_DIR, LLM_MODEL, TOP_K
from src.generation.answer import answer_question
from src.retrieval.embedder import get_model

EXAMPLES = [
    "What is the escape of water excess?",
    "Is my Northgate car covered for theft if I left the keys in it?",
    "How much will Harbourline pay for alternative accommodation?",
    "Who can authorise a claim worth £30,000?",
    "Does Northgate home insurance cover damage caused by a drone?",
]

STATUS_LABELS = {
    "answered": ("Answered from the documents", "green"),
    "referral": ("Not clearly settled by the documents - needs referral", "orange"),
    "not_found": ("Not found in the documents", "orange"),
    "uncited": ("Answer has no citations - verify before relying on it", "red"),
    "unsupported_figures": ("Contains figures not found in the cited sources - do not rely on it", "red"),
}

st.set_page_config(page_title="AI Document Assistant", page_icon="📄", layout="wide")


@st.cache_resource(show_spinner="Loading the embedding model...")
def warm_up():
    """Load the embedding model once when the app starts, not on the first question."""
    get_model()
    return True


def passage_pieces(chunk_text):
    """The pieces of text to look for on the PDF page.

    Skips the header line we added during chunking. Table rows were joined
    with ' | ' by our parser, so we look for each cell separately. Cells that
    are only a figure (like '£500') are skipped: the same figure may appear
    elsewhere on the page and we would highlight the wrong place.
    """
    pieces = []
    for line in chunk_text.split("\n")[1:]:
        line = line.lstrip("- ").strip()
        if " | " in line:
            pieces.extend(cell for cell in line.split(" | ")
                          if len(cell) > 3 and any(ch.isalpha() for ch in cell))
        elif line:
            pieces.append(line)
    return tuple(pieces)


@st.cache_data(show_spinner=False)
def render_page(filename, page_number, pieces):
    """Render one PDF page as an image, with the cited passage highlighted in yellow."""
    pdf = pymupdf.open(DOCUMENTS_DIR / filename)
    page = pdf[page_number - 1]

    # Short words like "Excess" can also appear higher up the page (e.g. in a heading).
    # Find where the passage starts, using its first longer line, and ignore matches above it.
    start_y = 0
    for piece in pieces:
        if len(piece) >= 25 and page.search_for(piece):
            start_y = page.search_for(piece)[0].y0 - 2
            break

    found = False
    for piece in pieces:
        areas = [a for a in page.search_for(piece) if a.y0 >= start_y]
        if areas:
            page.add_highlight_annot(areas)
            found = True
    image = page.get_pixmap(dpi=110).tobytes("png")
    return image, found


def filename_for(doc_id):
    return f"{doc_id}.pdf"


def show_citation(citation):
    label = (f"[{citation['number']}] {citation['insurer']} - {citation['title']} | "
             f"page {citation['page']}, section {citation['section']} ({citation['heading']})")
    with st.expander(label):
        left, right = st.columns([1, 1])
        with left:
            st.caption("Text the answer was based on")
            st.text(citation["text"].split("\n", 1)[-1])
        with right:
            image, found = render_page(filename_for(citation["doc_id"]), citation["page"],
                                       passage_pieces(citation["text"]))
            st.caption("Original page" + (" (cited text highlighted)" if found else ""))
            st.image(image, width="stretch")


def show_result(result):
    label, colour = STATUS_LABELS[result["status"]]
    st.markdown(f":{colour}[**{label}**]")
    st.markdown(result["answer"])
    if result.get("unsupported_figures"):
        st.error("Not in the cited sources: " + ", ".join(result["unsupported_figures"]))

    if result["citations"]:
        st.markdown("**Sources**")
        for citation in result["citations"]:
            show_citation(citation)

    with st.expander(f"All {len(result['sources'])} retrieved passages (for checking retrieval)"):
        for n, s in enumerate(result["sources"], start=1):
            st.markdown(f"**[{n}]** {s['insurer']} - {s['title']}, page {s['page']}, "
                        f"section {s['section']} ({s['heading']})")


# ---------------------------------------------------------------------------
# Sidebar: settings and example questions
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Settings")
    mode = st.selectbox("Search method", ["hybrid", "vector", "keyword"],
                        help="Hybrid combines meaning-based and keyword search.")
    auto_filter = st.toggle("Auto-filter by insurer and product", value=True,
                            help="If the question names an insurer or product, only search those documents.")
    top_k = st.slider("Passages given to the model", 1, 10, TOP_K)

    st.header("Try an example")
    for example in EXAMPLES:
        if st.button(example, width="stretch"):
            st.session_state.pending = example

    if st.button("Clear conversation", type="secondary"):
        st.session_state.history = []

    st.divider()
    st.caption(f"Model: {LLM_MODEL} (running locally)")
    st.caption("Documents are fictional and created for demonstration. "
               "Answers are not a cover decision.")

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
st.title("📄 AI Document Assistant")
st.write("Ask a question about the Northgate and Harbourline policy documents. "
         "Every answer shows where it came from.")

warm_up()
st.session_state.setdefault("history", [])

# Show previous questions and answers
for item in st.session_state.history:
    with st.chat_message("user"):
        st.write(item["question"])
    with st.chat_message("assistant"):
        show_result(item)

question = st.chat_input("e.g. What is the young driver excess on a Harbourline car policy?")
question = question or st.session_state.pop("pending", None)

if question:
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching the documents and writing an answer..."):
            result = answer_question(question, top_k=top_k, mode=mode, auto_filter=auto_filter)
        show_result(result)
    st.session_state.history.append(result)
