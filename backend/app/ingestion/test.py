
from app.ingestion.loader import load_pdfs_from_directory
from app.ingestion.chunker import chunk_documents
from app.ingestion.indexer import create_or_update_vector_store

docs = load_pdfs_from_directory("data/pdfs")
chunks = chunk_documents(docs)
create_or_update_vector_store(chunks)

print("Ingestion complete.")
print(f"Total documents loaded: {len(docs)}")
print(f"Total chunks created: {len(chunks)}")
