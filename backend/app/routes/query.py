from fastapi import APIRouter
import uuid

from app.models.schemas import QueryRequest, QueryResponse, SourceMetadata
from app.rag.retriever import get_relevant_chunks_with_scores
from app.rag.generator import generate_answer
from app.rag.confidence import compute_confidence
from app.config import CONFIDENCE_THRESHOLD, TOP_K
from app.models.db import load_queue, save_queue
from app.utils.logger import log_event

router = APIRouter()


@router.post("/", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    question = request.question.strip()

    # 1. Retrieve chunks WITH similarity scores
    results = get_relevant_chunks_with_scores(question, k=TOP_K)
    docs = [doc for doc, _ in results]

    # 2. Compute semantic confidence
    confidence = float(compute_confidence(results))

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
                    page=doc.metadata.get("page")
                )
            )

    # 4. If confidence is LOW → escalate immediately
    if confidence < CONFIDENCE_THRESHOLD:
        return _escalate(question, confidence, sources)

    # 5. Generate answer
    answer = generate_answer(docs, question).strip()

    # 6. LLM sanity check
    if answer.lower().startswith("i don't know"):
        return _escalate(question, 0.2, sources)

    # 7. Log ANSWERED query
    log_event({
        "type": "student_query",
        "question": question,
        "confidence": confidence,
        "action": "answered",
        "sources": [s.dict() for s in sources]
    })

    return QueryResponse(
        answer=answer,
        confidence=confidence,
        action="answered",
        sources=sources
    )


# ----------------------------------
# Helper: Escalation logic
# ----------------------------------
def _escalate(question: str, confidence: float, sources):
    queue = load_queue()

    ticket = {
        "id": str(uuid.uuid4()),
        "question": question,
        "confidence": float(confidence),
        "sources": [s.dict() for s in sources],
        "answer": None,
        "status": "pending"
    }

    queue.append(ticket)
    save_queue(queue)

    # 🔴 Log ESCALATION
    log_event({
        "type": "student_query",
        "question": question,
        "confidence": float(confidence),
        "action": "escalated",
        "sources": [s.dict() for s in sources],
        "ticket_id": ticket["id"]
    })

    return QueryResponse(
        answer="This question requires mentor review. A faculty member will respond shortly.",
        confidence=float(confidence),
        action="escalated",
        sources=sources
    )
