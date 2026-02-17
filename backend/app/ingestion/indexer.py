import os
from langchain_community.vectorstores import FAISS
from app.ingestion.embedder import get_embedding_model


VECTOR_STORE_PATH = "data/vector_store"


def create_or_update_vector_store(chunks):
    """
    Creates or updates FAISS vector store from chunks.
    """

    embeddings = get_embedding_model()

    if os.path.exists(VECTOR_STORE_PATH):
        vector_store = FAISS.load_local(
            VECTOR_STORE_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        vector_store.add_documents(chunks)
    else:
        vector_store = FAISS.from_documents(chunks, embeddings)

    vector_store.save_local(VECTOR_STORE_PATH)

    return vector_store
