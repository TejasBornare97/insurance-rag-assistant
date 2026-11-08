"""
Turn text into embeddings: lists of numbers that capture meaning.

Texts with similar meanings get similar numbers, even if they use
different words ("burst pipe" and "escape of water").
"""

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from src.config import EMBEDDING_MODEL


@lru_cache(maxsize=1)
def get_model():
    """Load the embedding model once and reuse it.

    The first call downloads the model (about 90 MB) and caches it on disk.
    lru_cache means later calls return the already-loaded model instantly.
    """
    return SentenceTransformer(EMBEDDING_MODEL)


def embed_texts(texts, show_progress=False):
    """Embed a list of texts. Returns one vector (list of floats) per text.

    normalize_embeddings=True scales every vector to length 1, so comparing two
    vectors is a simple dot product (this is called cosine similarity).
    """
    vectors = get_model().encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=show_progress,
        batch_size=32,
    )
    return vectors.tolist()


def embed_query(question):
    """Embed a single search question."""
    return embed_texts([question])[0]
