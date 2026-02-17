from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.query import router as query_router
from app.routes.ingest import router as ingest_router
from app.routes.mentor import router as mentor_router

app = FastAPI(title="Campus Mind Educational RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest_router, prefix="/ingest", tags=["Ingestion"])
app.include_router(query_router, prefix="/query", tags=["Query"])
app.include_router(mentor_router, prefix="/mentor", tags=["Mentor"])


@app.get("/")
def health_check():
    return {"status": "ok"}
