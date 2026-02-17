# from fastapi import APIRouter

# from app.models.schemas import QueryRequest, QueryResponse, SourceMetadata
# # from app.rag.retriever import get_relevant_chunks
# from app.rag.generator import generate_answer
# from app.rag.confidence import compute_confidence
# from app.config import CONFIDENCE_THRESHOLD, TOP_K


# # 
# from app.models.db import load_queue, save_queue
# import uuid

# # 
# from app.rag.retriever import get_relevant_chunks_with_scores

# router = APIRouter()


# @router.post("/", response_model=QueryResponse)
# def query_rag(request: QueryRequest):
#     question = request.question

#     # # 1. Retrieve relevant chunks
#     # docs = get_relevant_chunks(question, k=TOP_K)

#     # # 2. Compute confidence
#     # confidence = compute_confidence(docs)
#     results = get_relevant_chunks_with_scores(question, k=TOP_K)

#     docs = [doc for doc, _ in results]

#     confidence = compute_confidence(results)

#     # 3. Extract sources
#     sources = []
#     for doc in docs:
#         sources.append(
#             SourceMetadata(
#                 source=doc.metadata.get("source", "unknown"),
#                 page=doc.metadata.get("page")
#             )
#         )

#     # 4. Decide: answer or escalate
#     # if confidence < CONFIDENCE_THRESHOLD:
#     #     return QueryResponse(
#     #         answer="This question requires mentor review. I don't have enough confidence to answer from the provided material.",
#     #         confidence=confidence,
#     #         action="escalated",
#     #         sources=sources
#     #     )

#     if confidence < CONFIDENCE_THRESHOLD:
#         queue = load_queue()
        
#         ticket = {
#         "id": str(uuid.uuid4()),
#         "question": question,
#         "confidence": float(confidence),
#         "sources": [s.dict() for s in sources],
#         "answer": None,
#         "status": "pending"
#       }
#         queue.append(ticket)
#         save_queue(queue)
        
#         return QueryResponse(
#         answer="This question requires mentor review. A faculty member will respond shortly.",
#         confidence=confidence,
#         action="escalated",
#         sources=sources
#        )

#     # 5. Generate answer
#     answer = generate_answer(docs, question)

#     return QueryResponse(
#         answer=answer,
#         confidence=confidence,
#         action="answered",
#         sources=sources
#     )

# ////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////

# from fastapi import APIRouter

# from app.models.schemas import QueryRequest, QueryResponse, SourceMetadata
# from app.rag.retriever import get_relevant_chunks_with_scores
# from app.rag.generator import generate_answer
# from app.rag.confidence import compute_confidence
# from app.config import CONFIDENCE_THRESHOLD, TOP_K
# from app.models.db import load_queue, save_queue

# import uuid
# # 
# from app.utils.logger import log_event

# router = APIRouter()


# @router.post("/", response_model=QueryResponse)
# def query_rag(request: QueryRequest):
#     question = request.question.strip()

#     # 1. Retrieve chunks WITH similarity scores
#     results = get_relevant_chunks_with_scores(question, k=TOP_K)

#     docs = [doc for doc, _ in results]

#     # 2. Compute semantic confidence
#     confidence = float(compute_confidence(results))

#     # 3. Extract & deduplicate sources
#     seen = set()
#     sources = []
#     for doc in docs:
#         key = (doc.metadata.get("source"), doc.metadata.get("page"))
#         if key not in seen:
#             seen.add(key)
#             sources.append(
#                 SourceMetadata(
#                     source=doc.metadata.get("source", "unknown"),
#                     page=doc.metadata.get("page")
#                 )
#             )

#     # 4. If confidence is LOW → escalate immediately
#     if confidence < CONFIDENCE_THRESHOLD:
#         return _escalate(question, confidence, sources)

#     # 5. Generate answer (LLM is used ONLY after passing confidence gate)
#     answer = generate_answer(docs, question).strip()

#     # 6. Sanity check:
#     # If LLM itself says "I don't know", this is NOT a valid answer
#     if answer.lower().startswith("i don't know"):
#         return _escalate(question, 0.2, sources)

#     # 7. Valid grounded answer
#     return QueryResponse(
#         answer=answer,
#         confidence=confidence,
#         action="answered",
#         sources=sources
#     )


# # -------------------------------
# # Helper: Escalation logic
# # -------------------------------
# def _escalate(question: str, confidence: float, sources):
#     queue = load_queue()

#     ticket = {
#         "id": str(uuid.uuid4()),
#         "question": question,
#         "confidence": float(confidence),
#         "sources": [s.dict() for s in sources],
#         "answer": None,
#         "status": "pending"
#     }

#     queue.append(ticket)
#     save_queue(queue)

#     return QueryResponse(
#         answer="This question requires mentor review. A faculty member will respond shortly.",
#         confidence=float(confidence),
#         action="escalated",
#         sources=sources
#     )

# ////////////////////////////////////////////////////
# ////////////////////////////////////////////////////


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
