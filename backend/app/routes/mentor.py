"""
Mentor Routes
=============
Endpoints for the mentor/faculty dashboard:
  GET  /mentor/pending          — Fetch unanswered questions
  POST /mentor/answer/{id}      — Submit a verified answer
  GET  /mentor/answered         — Fetch all verified answers
"""

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.db import load_queue, save_queue
from app.utils.logger import log_event

logger = logging.getLogger(__name__)
router = APIRouter()


class MentorAnswerRequest(BaseModel):
    answer: str


@router.get("/pending")
def get_pending_questions():
    """Mentor fetches unanswered questions."""
    queue = load_queue()
    pending = [q for q in queue if q["status"] == "pending"]
    logger.info("Fetched %d pending tickets.", len(pending))
    return pending


@router.post("/answer/{ticket_id}")
def answer_question(ticket_id: str, request: MentorAnswerRequest):
    """Mentor submits verified answer for a ticket."""
    if not request.answer.strip():
        raise HTTPException(status_code=400, detail="Answer cannot be empty.")

    queue = load_queue()

    for q in queue:
        if q["id"] == ticket_id:
            q["answer"] = request.answer
            q["status"] = "answered"
            save_queue(queue)

            log_event({
                "type": "mentor_response",
                "ticket_id": ticket_id,
                "answer": request.answer,
            })

            logger.info("Mentor answered ticket: %s", ticket_id)
            return {"message": "Answer submitted successfully"}

    raise HTTPException(status_code=404, detail="Ticket not found")


@router.get("/answered")
def get_answered_questions():
    """Fetch mentor-answered (verified) questions for students."""
    queue = load_queue()

    answered = [
        {
            "id": q["id"],
            "question": q["question"],
            "answer": q["answer"],
            "confidence": q.get("confidence", 0),
            "sources": q.get("sources", []),
        }
        for q in queue
        if q.get("status") == "answered" and q.get("answer")
    ]

    logger.info("Fetched %d verified answers.", len(answered))
    return answered
