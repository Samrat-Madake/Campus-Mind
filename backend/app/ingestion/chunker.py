from langchain_text_splitters import RecursiveCharacterTextSplitter
# from typing import List
import re


# TEXT CLEANING
# =========================
def clean_pdf_text(text: str) -> str:
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = re.sub(r"●", "\n- ", text)
    text = re.sub(r"-\s+", "- ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()



def chunk_documents(documents):
    """
    Splits documents into semantically meaningful chunks.
    """
    
    # for doc in documents:
    #     doc.metadata["source"] = pdf_path
    #     doc.page_content = clean_pdf_text(doc.page_content)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " "]
    )

    chunks = text_splitter.split_documents(documents)

    # Apply cleaning AFTER chunking
    for chunk in chunks:
        chunk.page_content = clean_pdf_text(chunk.page_content)
    
    return chunks
