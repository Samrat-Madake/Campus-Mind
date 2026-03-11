"""
Hybrid Retrieval Engine
=======================
5-stage retrieval pipeline:
  1. MultiQuery expansion (LLM generates reformulated queries)
  2. MMR vector search (relevance + diversity)
  3. BM25 keyword search (exact term matching)
  4. Hybrid ensemble (50/50 weighted combination)
  5. Cross-encoder reranking (precise relevance scoring)

All models are loaded from the singleton ModelService — no per-request loading.
"""

import logging

from langchain_classic.retrievers import MultiQueryRetriever, EnsembleRetriever

from app.services.model_service import ModelService
from app.core.settings import RERANKER_TOP_K, RETRIEVER_CANDIDATE_LIMIT
from app.core.exceptions import VectorStoreNotFoundError

logger = logging.getLogger(__name__)


def _ensure_vectorstore():
    """Raise if vector store is not loaded."""
    ms = ModelService.get()
    if not ms.is_ready:
        raise VectorStoreNotFoundError(
            "Vector store is not loaded. Ingest documents first."
        )
    return ms


# ─────────────────────────────────────────────
# Reranking
# ─────────────────────────────────────────────
def rerank_documents(query: str, docs, top_k: int = RERANKER_TOP_K):
    """Rerank documents using Cross-Encoder for precise relevance scoring."""
    ms = ModelService.get()

    pairs = [[query, doc.page_content] for doc in docs]
    scores = ms.reranker.predict(pairs)

    scored_docs = list(zip(docs, scores))
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    return scored_docs[:top_k]


# ─────────────────────────────────────────────
# Hybrid Retrieval: MultiQuery + MMR + BM25 + Reranker
# ─────────────────────────────────────────────
def get_multiquery_mmr_BM25_with_scores(query: str, k: int = 6):
    """
    Full hybrid retrieval pipeline:
    MultiQuery → MMR → BM25 → Ensemble → Reranker → Top-K
    """
    ms = _ensure_vectorstore()

    # MMR retriever (40% relevance, 60% diversity)
    mmr_retriever = ms.vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "lambda_mult": 0.4},
    )

    # MultiQuery wrapper (LLM generates alternative queries)
    multiquery = MultiQueryRetriever.from_llm(
        retriever=mmr_retriever,
        llm=ms.llm,
    )

    # Hybrid: MultiQuery+MMR (50%) + BM25 (50%)
    hybrid_retriever = EnsembleRetriever(
        retrievers=[multiquery, ms.bm25_retriever],
        weights=[0.5, 0.5],
    )

    docs = hybrid_retriever.invoke(query)

    # Limit candidates before expensive reranking
    docs = docs[:RETRIEVER_CANDIDATE_LIMIT]

    logger.info(
        "Retrieved %d candidates for query: '%s' (truncated to %d)",
        len(docs),
        query[:80],
        RETRIEVER_CANDIDATE_LIMIT,
    )

    reranked_docs = rerank_documents(query, docs, top_k=RERANKER_TOP_K)

    return reranked_docs


# ─────────────────────────────────────────────
# Public Entry Point
# ─────────────────────────────────────────────
def get_relevant_chunks_with_scores(query: str, k: int = 5):
    """
    Single entry point for the query route.
    Returns: [(Document, reranker_score), ...]
    """
    return get_multiquery_mmr_BM25_with_scores(query, k=k)