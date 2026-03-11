"""
Singleton Model Service
=======================
Loads all heavy AI models ONCE at application startup and keeps them in memory.

Before:  Every request loaded CrossEncoder (~500MB), FAISS, BM25, LLM → 15-30s per query.
After:   Models loaded once → queries take ~2-5s.

Usage:
    from app.services.model_service import ModelService

    # At startup (called from main.py):
    ModelService.initialize()

    # In any route/module:
    ms = ModelService.get()
    ms.vectorstore.similarity_search(...)
    ms.reranker.predict(...)
    ms.llm.invoke(...)
"""

import logging
import os

from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from sentence_transformers import CrossEncoder

from app.core.settings import (
    GROQ_API_KEY,
    EMBEDDING_MODEL,
    RERANKER_MODEL,
    LLM_MODEL,
    LLM_TEMPERATURE,
    VECTOR_STORE_PATH,
)
from app.core.exceptions import VectorStoreNotFoundError

logger = logging.getLogger(__name__)


class ModelService:
    """
    Singleton that holds all heavy AI models in memory.
    Call initialize() once at startup, then use get() anywhere.
    """

    _instance: "ModelService | None" = None

    def __init__(self):
        # ── Embedding Model ──────────────────────────
        logger.info("Loading embedding model: %s", EMBEDDING_MODEL)
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            encode_kwargs={"normalize_embeddings": True},
        )

        # ── Cross-Encoder Reranker ───────────────────
        logger.info("Loading reranker model: %s", RERANKER_MODEL)
        self.reranker = CrossEncoder(RERANKER_MODEL)

        # ── LLM ──────────────────────────────────────
        logger.info("Initializing LLM: %s (temperature=%.2f)", LLM_MODEL, LLM_TEMPERATURE)
        self.llm = ChatGroq(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            groq_api_key=GROQ_API_KEY,
        )

        # ── FAISS Vector Store ───────────────────────
        self.vectorstore = None
        self.bm25_retriever = None
        self._load_vectorstore()

    # ─────────────────────────────────────────────────
    # Vector Store & BM25 Loading
    # ─────────────────────────────────────────────────
    def _load_vectorstore(self):
        """Load FAISS vector store and build BM25 index from it."""
        if not os.path.exists(VECTOR_STORE_PATH):
            logger.warning(
                "Vector store not found at %s. "
                "Queries will fail until documents are ingested.",
                VECTOR_STORE_PATH,
            )
            self.vectorstore = None
            self.bm25_retriever = None
            return

        logger.info("Loading FAISS vector store from: %s", VECTOR_STORE_PATH)
        self.vectorstore = FAISS.load_local(
            VECTOR_STORE_PATH,
            self.embedding_model,
            allow_dangerous_deserialization=True,
        )

        # Build BM25 index from FAISS documents
        logger.info("Building BM25 index from vector store documents...")
        docs = list(self.vectorstore.docstore._dict.values())
        self.bm25_retriever = BM25Retriever.from_documents(docs)
        self.bm25_retriever.k = 5
        logger.info("BM25 index built with %d documents.", len(docs))

    def reload_vectorstore(self):
        """
        Reload FAISS and BM25 after new documents are ingested.
        Called after ingestion endpoint processes new PDFs.
        """
        logger.info("Reloading vector store after ingestion...")
        self._load_vectorstore()
        logger.info("Vector store reloaded successfully.")

    @property
    def is_ready(self) -> bool:
        """Check if the vector store is loaded and ready for queries."""
        return self.vectorstore is not None

    # ─────────────────────────────────────────────────
    # Singleton Access
    # ─────────────────────────────────────────────────
    @classmethod
    def initialize(cls):
        """
        Initialize the singleton. Call once at app startup.
        Subsequent calls are no-ops.
        """
        if cls._instance is not None:
            logger.info("ModelService already initialized, skipping.")
            return
        logger.info("=" * 50)
        logger.info("INITIALIZING MODEL SERVICE")
        logger.info("=" * 50)
        cls._instance = cls()
        logger.info("=" * 50)
        logger.info("MODEL SERVICE READY")
        logger.info("=" * 50)

    @classmethod
    def get(cls) -> "ModelService":
        """
        Get the singleton instance.
        Raises RuntimeError if initialize() hasn't been called.
        """
        if cls._instance is None:
            raise RuntimeError(
                "ModelService not initialized. Call ModelService.initialize() "
                "at application startup."
            )
        return cls._instance
