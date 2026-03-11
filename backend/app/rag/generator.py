"""
LLM Answer Generator
====================
Generates grounded answers from retrieved documents using the singleton LLM.
"""

import logging

from app.rag.prompt import STRICT_RAG_PROMPT
from app.services.model_service import ModelService
from app.core.exceptions import LLMServiceError

logger = logging.getLogger(__name__)


def generate_answer(context_docs, question: str) -> str:
    """
    Generates grounded answer from retrieved documents.
    Uses the singleton LLM instance from ModelService.
    """
    ms = ModelService.get()

    context_text = "\n\n".join([doc.page_content for doc in context_docs])

    prompt = STRICT_RAG_PROMPT.format(
        context=context_text,
        question=question,
    )

    try:
        response = ms.llm.invoke(prompt)
        return response.content
    except Exception as e:
        logger.error("LLM generation failed: %s", e)
        raise LLMServiceError(f"Failed to generate answer: {e}") from e
