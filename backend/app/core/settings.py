import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# ──────────────────────────────────────────────
# Resolve base directory (backend/)
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # backend/

# ──────────────────────────────────────────────
# API Keys
# ──────────────────────────────────────────────
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
HUGGINGFACEHUB_API_TOKEN: str = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")

# ──────────────────────────────────────────────
# RAG Settings
# ──────────────────────────────────────────────
CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.55"))
TOP_K: int = int(os.getenv("TOP_K", "4"))
RERANKER_TOP_K: int = int(os.getenv("RERANKER_TOP_K", "5"))
RETRIEVER_CANDIDATE_LIMIT: int = int(os.getenv("RETRIEVER_CANDIDATE_LIMIT", "10"))
MAX_QUESTION_LENGTH: int = int(os.getenv("MAX_QUESTION_LENGTH", "500"))

# ──────────────────────────────────────────────
# Model Configuration
# ──────────────────────────────────────────────
LLM_MODEL: str = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.4"))
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")
RERANKER_MODEL: str = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-base")

# ──────────────────────────────────────────────
# Paths (resolved relative to BASE_DIR)
# ──────────────────────────────────────────────
VECTOR_STORE_PATH: str = str(BASE_DIR / "data" / "vector_store")
MENTOR_QUEUE_PATH: str = str(BASE_DIR / "data" / "mentor_queue.json")
AUDIT_LOG_PATH: str = str(BASE_DIR / "data" / "audit_logs.json")
PDF_DIRECTORY: str = str(BASE_DIR / "data" / "pdfs")
PDF_MAX_SIZE_MB: int = int(os.getenv("PDF_MAX_SIZE_MB", "50"))
