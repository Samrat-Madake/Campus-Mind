from langchain_community.document_loaders import PyPDFLoader
from typing import List
import os


def load_pdfs_from_directory(directory_path: str):
    """
    Loads all PDFs from a directory and returns LangChain Documents.
    """
    documents = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)

            loader = PyPDFLoader(file_path)
            pdf_docs = loader.load()

            # add source metadata
            for doc in pdf_docs:
                doc.metadata["source"] = filename

            documents.extend(pdf_docs)

    return documents
