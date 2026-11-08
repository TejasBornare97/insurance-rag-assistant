from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = ROOT_DIR / "data" / "raw"
DOCUMENTS_DIR = ROOT_DIR / "data" / "documents"
CHROMA_DIR = ROOT_DIR / "chroma_db"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "llama3.1:8b"
COLLECTION_NAME = "insurance_policies"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
TOP_K = 5