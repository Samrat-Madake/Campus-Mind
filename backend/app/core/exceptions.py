"""
Custom exception classes for Campus Mind backend.
"""


class VectorStoreNotFoundError(Exception):
    """Raised when FAISS vector store files are missing."""

    def __init__(self, path: str):
        self.path = path
        super().__init__(f"Vector store not found at: {path}")


class IngestionError(Exception):
    """Raised when document ingestion fails."""
    pass


class LLMServiceError(Exception):
    """Raised when the LLM API call fails."""
    pass


class EmptyQueryError(Exception):
    """Raised when a student submits an empty/invalid question."""
    pass
