"""
Student Query Route
===================
POST /query/ — Handles student questions through the RAG pipeline.

Pipeline:
  1. Validate input
  2. Retrieve relevant chunks (hybrid retrieval + reranking)
  3. Compute semantic confidence
  4. If low confidence → escalate to mentor
  5. Generate LLM answer
  6. Sanity check (LLM says "I don't know" → escalate anyway)
  7. Log audit event and return response
"""

import logging
import uuid

from fastapi import APIRouter

from app.models.schemas import QueryRequest, QueryResponse, SourceMetadata
from app.rag.retriever import get_relevant_chunks_with_scores
from app.rag.generator import generate_answer
from app.rag.confidence import compute_confidence
from app.core.settings import CONFIDENCE_THRESHOLD, TOP_K, MAX_QUESTION_LENGTH
from app.core.exceptions import EmptyQueryError
from app.models.db import load_queue, save_queue
from app.utils.logger import log_event

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    question = request.question.strip()

    # ── Input Validation ──────────────────────────
    if not question:
        raise EmptyQueryError("Question cannot be empty.")
    if len(question) > MAX_QUESTION_LENGTH:
        raise EmptyQueryError(
            f"Question is too long ({len(question)} chars). "
            f"Maximum allowed: {MAX_QUESTION_LENGTH} characters."
        )

    logger.info("Processing query: '%s'", question[:80])

    # 1. Retrieve chunks WITH similarity scores
    results = get_relevant_chunks_with_scores(question, k=TOP_K)
    docs = [doc for doc, _ in results]

    # 2. Compute semantic confidence
    confidence = float(compute_confidence(results))
    logger.info("Confidence score: %.2f (threshold: %.2f)", confidence, CONFIDENCE_THRESHOLD)

    # 3. Extract & deduplicate sources
    seen = set()
    sources = []
    for doc in docs:
        key = (doc.metadata.get("source"), doc.metadata.get("page"))
        if key not in seen:
            seen.add(key)
            sources.append(
                SourceMetadata(
                    source=doc.metadata.get("source", "unknown"),
                    page=doc.metadata.get("page"),
                )
            )

    # 4. If confidence is LOW → escalate immediately
    if confidence < CONFIDENCE_THRESHOLD:
        logger.info("Low confidence (%.2f) — escalating to mentor.", confidence)
        return _escalate(question, confidence, sources)

    # 5. Generate answer
    answer = generate_answer(docs, question).strip()

    # 6. LLM sanity check
    if answer.lower().startswith("i don't know"):
        logger.info("LLM returned 'I don't know' — escalating to mentor.")
        return _escalate(question, 0.2, sources)

    # 7. Log ANSWERED query
    log_event({
        "type": "student_query",
        "question": question,
        "confidence": confidence,
        "action": "answered",
        "sources": [s.dict() for s in sources],
    })

    logger.info("Query answered successfully (confidence=%.2f).", confidence)

    return QueryResponse(
        answer=answer,
        confidence=confidence,
        action="answered",
        sources=sources,
    )


# ──────────────────────────────────────────────
# Helper: Escalation logic
# ──────────────────────────────────────────────
def _escalate(question: str, confidence: float, sources):
    """Create a mentor ticket, log the escalation, return escalation response."""
    queue = load_queue()

    ticket = {
        "id": str(uuid.uuid4()),
        "question": question,
        "confidence": float(confidence),
        "sources": [s.dict() for s in sources],
        "answer": None,
        "status": "pending",
    }

    queue.append(ticket)
    save_queue(queue)

    log_event({
        "type": "student_query",
        "question": question,
        "confidence": float(confidence),
        "action": "escalated",
        "sources": [s.dict() for s in sources],
        "ticket_id": ticket["id"],
    })

    return QueryResponse(
        answer="This question requires mentor review. A faculty member will respond shortly.",
        confidence=float(confidence),
        action="escalated",
        sources=sources,
    )
