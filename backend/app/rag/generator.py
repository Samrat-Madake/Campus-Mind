# from langchain_openai import ChatOpenAI

from app.rag.prompt import STRICT_RAG_PROMPT
from app.dependencies import get_llm


def generate_answer(context_docs, question: str):
    """
    Generates grounded answer from retrieved documents.
    """

    llm = get_llm()

    context_text = "\n\n".join(
        [doc.page_content for doc in context_docs]
    )

    prompt = STRICT_RAG_PROMPT.format(
        context=context_text,
        question=question
    )

    response = llm.invoke(prompt)

    return response.content
