from langchain_community.vectorstores import FAISS
from app.ingestion.embedder import get_embedding_model

embeddings = get_embedding_model()
db = FAISS.load_local(
    "data/vector_store",
    embeddings,
    allow_dangerous_deserialization=True
)

results = db.similarity_search("What is Decession Tree binning?", k=5)

for r in results:
    print(r.page_content[:200])
    print("SOURCE:", r.metadata)
    print("-" * 50)
