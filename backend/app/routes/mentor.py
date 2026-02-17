

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.db import load_queue, save_queue
from app.utils.logger import log_event

router = APIRouter()


class MentorAnswerRequest(BaseModel):
    answer: str


@router.get("/pending")
def get_pending_questions():
    """
    Mentor fetches unanswered questions.
    """
    queue = load_queue()
    return [q for q in queue if q["status"] == "pending"]


@router.post("/answer/{ticket_id}")
def answer_question(ticket_id: str, request: MentorAnswerRequest):
    """
    Mentor submits verified answer.
    """
    queue = load_queue()

    for q in queue:
        if q["id"] == ticket_id:
            q["answer"] = request.answer
            q["status"] = "answered"
            save_queue(queue)

            # 🟢 Log mentor response
            log_event({
                "type": "mentor_response",
                "ticket_id": ticket_id,
                "answer": request.answer
            })

            return {"message": "Answer submitted successfully"}

    raise HTTPException(status_code=404, detail="Ticket not found")


# 
@router.get("/answered")
def get_answered_questions():
    """
    Fetch mentor-answered (verified) questions.
    Visible to students as verified answers.
    """
    queue = load_queue()

    answered = [
        {
            "id": q["id"],
            "question": q["question"],
            "answer": q["answer"],
            "confidence": q.get("confidence", 0),
            "sources": q.get("sources", [])
        }
        for q in queue
        if q.get("status") == "answered" and q.get("answer")
    ]

    return answered
