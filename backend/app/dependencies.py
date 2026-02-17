import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()


def get_llm():
    """
    Returns ChatGroq LLM instance.
    """
    print("GROQ KEY LOADED:", os.getenv("GROQ_API_KEY") is not None)
    return ChatGroq(
        # model="llama3-8b-8192",
        model="llama-3.1-8b-instant",
        temperature=0.4,   # IMPORTANT for education
        groq_api_key=os.getenv("GROQ_API_KEY")
    )


def get_embedding_model():
    """
    Returns HuggingFace SentenceTransformer embeddings.
    """
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
