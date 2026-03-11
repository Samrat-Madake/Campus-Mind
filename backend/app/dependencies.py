"""
DEPRECATED — Use app.services.model_service.ModelService instead.
This file is kept for backwards compatibility only.
"""
from app.core.settings import GROQ_API_KEY, LLM_MODEL, LLM_TEMPERATURE, EMBEDDING_MODEL

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings


def get_llm():
    """Returns ChatGroq LLM instance. Prefer ModelService.get().llm instead."""
    return ChatGroq(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        groq_api_key=GROQ_API_KEY,
    )


def get_embedding_model():
    """Returns HuggingFace embedding model. Prefer ModelService.get().embedding_model instead."""
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        encode_kwargs={"normalize_embeddings": True},
    )
