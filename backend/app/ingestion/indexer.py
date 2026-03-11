"""
FAISS Indexer
=============
Creates or updates the FAISS vector store from document chunks.
Uses the singleton embedding model from ModelService when available,
or creates a fresh embedding model during initial ingestion.
"""

import logging
import os

from langchain_community.vectorstores import FAISS

from app.core.settings import VECTOR_STORE_PATH, EMBEDDING_MODEL

logger = logging.getLogger(__name__)


def _get_embeddings():
    """
    Get embedding model — from ModelService if initialized,
    otherwise create a fresh one (for standalone ingestion scripts).
    """
    try:
        from app.services.model_service import ModelService
        ms = ModelService.get()
        return ms.embedding_model
    except (RuntimeError, Exception):
        # ModelService not initialized (running standalone script)
        from langchain_huggingface import HuggingFaceEmbeddings
        logger.info("ModelService not available, creating fresh embedding model.")
        return HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            encode_kwargs={"normalize_embeddings": True},
        )


def create_or_update_vector_store(chunks):
    """
    Creates or updates FAISS vector store from document chunks.
    Supports incremental ingestion (appends to existing store).
    """
    embeddings = _get_embeddings()

    if os.path.exists(VECTOR_STORE_PATH):
        logger.info("Loading existing vector store for incremental update...")
        vector_store = FAISS.load_local(
            VECTOR_STORE_PATH,
            embeddings,
            allow_dangerous_deserialization=True,
        )
        vector_store.add_documents(chunks)
        logger.info("Added %d new chunks to existing vector store.", len(chunks))
    else:
        logger.info("Creating new vector store with %d chunks...", len(chunks))
        vector_store = FAISS.from_documents(chunks, embeddings)

    vector_store.save_local(VECTOR_STORE_PATH)
    logger.info("Vector store saved to: %s", VECTOR_STORE_PATH)

    return vector_store
