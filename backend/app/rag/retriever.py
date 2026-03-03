from langchain_community.vectorstores import FAISS
from langchain_classic.retrievers import MultiQueryRetriever

from app.dependencies import get_llm
from app.ingestion.embedder import get_embedding_model

VECTOR_STORE_PATH = "data/vector_store"



# ---------------------------------------------------
# Load Vector Store
# ---------------------------------------------------
def load_vectorstore():
    embeddings = get_embedding_model()

    db = FAISS.load_local(
        VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db


# ---------------------------------------------------
# 1️⃣ Basic Similarity Retriever (with scores)
# ---------------------------------------------------
# def get_similarity_chunks_with_scores(query: str, k: int = 4):
#     """
#     Standard similarity search.
#     Returns: [(Document, score)]
#     Lower score = better match.
#     """
#     db = load_vectorstore()
#     return db.similarity_search_with_score(query, k=k)


# ---------------------------------------------------
# 2️⃣ MMR Retriever (diversity-aware retrieval)
# ---------------------------------------------------
# def get_mmr_retriever(k: int = 4, lambda_mult: float = 0.4):
#     """
#     MMR = Maximum Marginal Relevance
#     Balances relevance + diversity.
#     """

#     db = load_vectorstore()

#     mmr_retriever = db.as_retriever(
#         search_type="mmr",
#         search_kwargs={
#             "k": k,
#             "lambda_mult": lambda_mult
#         }
#     )

#     return mmr_retriever


# ---------------------------------------------------
# 3️⃣ MultiQuery Retriever
# ---------------------------------------------------
# def get_multiquery_retriever(k: int = 4):
#     """
#     MultiQuery = Generates multiple reformulated queries using LLM
#     """

#     db = load_vectorstore()
#     llm = get_llm()

#     base_retriever = db.as_retriever(search_kwargs={"k": k})

#     multiquery_retriever = MultiQueryRetriever.from_llm(
#         retriever=base_retriever,
#         llm=llm
#     )

#     return multiquery_retriever


# ---------------------------------------------------
# 4️⃣ MultiQuery + MMR +Scores (Advanced Retrieval)
# ---------------------------------------------------
def get_multiquery_mmr_with_scores(query: str, k: int = 4):
    db = load_vectorstore()
    llm = get_llm()

    # Step 1: MMR retriever
    # mmr_retriever = db.as_retriever(
    #     search_type="mmr",
    #     search_kwargs={"k": k}
    # )
    mmr_retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": k,
            "lambda_mult": 0.4
        }
    )

    # Step 2: MultiQuery wrapper
    multiquery = MultiQueryRetriever.from_llm(
        retriever=mmr_retriever,
        llm=llm
    )

    # Step 3: Get documents
    docs = multiquery.invoke(query)

    # Step 4: Re-score manually
    results = []
    for doc in docs:
        score = db.similarity_search_with_score(doc.page_content, k=1)[0][1]
        results.append((doc, score))

    return results



# ---------------------------------------------------
# ---------------------------------------------------
def get_relevant_chunks_with_scores(query: str, k: int = 5):
    return get_multiquery_mmr_with_scores(query, k=k)

'''
🧠 What MMR Actually Optimizes

Conceptually, MMR selects documents using:


MMR= λ x Relevance - (1 - λ) x Redundancy

Where:

Relevance = similarity to user query

Redundancy = similarity to already selected documents

λ (lambda_mult) = balance factor

OUR CASE:  λ : 0.4 
40% relevance
60% diversity consideration
'''

 
    

#  OLD VERSION 
# def get_relevant_chunks_with_scores(query: str, k: int = 4):
#     """
#     Retrieves top-k chunks WITH similarity scores.
#     Lower score = better match.
#     """
#     embeddings = get_embedding_model()

#     db = FAISS.load_local(
#         VECTOR_STORE_PATH,
#         embeddings,
#         allow_dangerous_deserialization=True
#     )

#     results = db.similarity_search_with_score(query, k=k)
#     return results  # [(Document, score), ...]