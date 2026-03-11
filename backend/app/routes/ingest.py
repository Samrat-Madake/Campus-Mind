"""
Ingestion Route
===============
POST /ingest/upload — Upload a PDF file for ingestion into the RAG knowledge base.

Flow:
  1. Validate file (must be PDF, max size check)
  2. Save to data/pdfs/
  3. Run ingestion pipeline (load → chunk → embed → index)
  4. Reload in-memory vector store and BM25 index
  5. Return chunk count and status
"""

import logging
import os

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.core.settings import PDF_DIRECTORY, PDF_MAX_SIZE_MB
from app.ingestion.loader import load_pdfs_from_directory
from app.ingestion.chunker import chunk_documents
from app.ingestion.indexer import create_or_update_vector_store
from app.services.model_service import ModelService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload")
async def upload_and_ingest(file: UploadFile = File(...)):
    """
    Upload a PDF file and ingest it into the vector store.
    """
    # ── Validate file type ──────────────────
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted.",
        )

    # ── Read file content ───────────────────
    content = await file.read()

    # ── Validate file size ──────────────────
    max_bytes = PDF_MAX_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {PDF_MAX_SIZE_MB}MB.",
        )

    # ── Save file to data/pdfs/ ─────────────
    os.makedirs(PDF_DIRECTORY, exist_ok=True)
    file_path = os.path.join(PDF_DIRECTORY, file.filename)

    with open(file_path, "wb") as f:
        f.write(content)
    logger.info("Saved uploaded PDF: %s (%d bytes)", file.filename, len(content))

    # ── Run ingestion pipeline ──────────────
    try:
        docs = load_pdfs_from_directory(PDF_DIRECTORY)
        chunks = chunk_documents(docs)
        create_or_update_vector_store(chunks)

        logger.info(
            "Ingestion complete: %d documents, %d chunks",
            len(docs),
            len(chunks),
        )

        # ── Reload in-memory models ─────────
        ms = ModelService.get()
        ms.reload_vectorstore()

        return {
            "status": "success",
            "filename": file.filename,
            "documents_loaded": len(docs),
            "chunks_created": len(chunks),
            "message": f"Successfully ingested {file.filename}. "
                       f"Vector store updated with {len(chunks)} chunks.",
        }

    except Exception as e:
        logger.error("Ingestion failed for %s: %s", file.filename, e)
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}",
        )
