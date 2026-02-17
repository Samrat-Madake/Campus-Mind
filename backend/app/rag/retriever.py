# from langchain_community.vectorstores import FAISS
# from app.ingestion.embedder import get_embedding_model

# VECTOR_STORE_PATH = "data/vector_store"


# def get_relevant_chunks(query: str, k: int = 4):
#     """
#     Retrieves top-k relevant chunks for a query.
#     """

#     embeddings = get_embedding_model()

#     db = FAISS.load_local(
#         VECTOR_STORE_PATH,
#         embeddings,
#         allow_dangerous_deserialization=True
#     )

#     docs = db.similarity_search(query, k=k)
#     return docs

from langchain_community.vectorstores import FAISS
from app.ingestion.embedder import get_embedding_model

VECTOR_STORE_PATH = "data/vector_store"


def get_relevant_chunks_with_scores(query: str, k: int = 4):
    """
    Retrieves top-k chunks WITH similarity scores.
    Lower score = better match.
    """
    embeddings = get_embedding_model()

    db = FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    results = db.similarity_search_with_score(query, k=k)
    return results  # [(Document, score), ...]
