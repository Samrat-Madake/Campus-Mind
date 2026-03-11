import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes.query import router as query_router
from app.routes.ingest import router as ingest_router
from app.routes.mentor import router as mentor_router
from app.services.model_service import ModelService
from app.core.exceptions import (
    VectorStoreNotFoundError,
    EmptyQueryError,
    LLMServiceError,
)

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Configure logging at module level
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# ──────────────────────────────────────────────
# Lifespan: startup / shutdown events
# ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── STARTUP ──
    logger.info("Starting Campus Mind backend...")
    ModelService.initialize()
    logger.info("Campus Mind backend is ready.")
    yield
    # ── SHUTDOWN ──
    logger.info("Shutting down Campus Mind backend.")


# ──────────────────────────────────────────────
# App Factory
# ──────────────────────────────────────────────
app = FastAPI(title="Campus Mind Educational RAG", lifespan=lifespan)

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


# ──────────────────────────────────────────────
# Global Exception Handlers
# ──────────────────────────────────────────────
@app.exception_handler(VectorStoreNotFoundError)
async def vectorstore_not_found_handler(request: Request, exc: VectorStoreNotFoundError):
    logger.error("Vector store not found: %s", exc.path)
    return JSONResponse(
        status_code=503,
        content={
            "error": "service_unavailable",
            "message": "The knowledge base has not been set up yet. Please ingest documents first.",
        },
    )


@app.exception_handler(EmptyQueryError)
async def empty_query_handler(request: Request, exc: EmptyQueryError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "invalid_query",
            "message": str(exc),
        },
    )


@app.exception_handler(LLMServiceError)
async def llm_service_handler(request: Request, exc: LLMServiceError):
    logger.error("LLM service error: %s", exc)
    return JSONResponse(
        status_code=503,
        content={
            "error": "llm_unavailable",
            "message": "The AI service is temporarily unavailable. Please try again shortly.",
        },
    )


# ──────────────────────────────────────────────
# Health Check
# ──────────────────────────────────────────────
@app.get("/")
def health_check():
    ms = ModelService.get()
    return {
        "status": "ok",
        "vectorstore_loaded": ms.is_ready,
    }
