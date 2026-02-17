from pydantic import BaseModel
from typing import List, Optional


class QueryRequest(BaseModel):
    question: str


class SourceMetadata(BaseModel):
    source: str
    page: Optional[int]


class QueryResponse(BaseModel):
    answer: str
    confidence: float
    action: str  # "answered" | "escalated"
    sources: List[SourceMetadata]
