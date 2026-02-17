from app.rag.retriever import get_relevant_chunks
from app.rag.generator import generate_answer
from app.rag.confidence import compute_confidence

# question = "What is exploratory data analysis?"
question = "What is Importance of the Curse of Dimensionality?"

docs = get_relevant_chunks(question)
confidence = compute_confidence(docs)

print("Confidence:", confidence)

if confidence < 0.6:
    print("Escalate to mentor")
else:
    answer = generate_answer(docs, question)
    print(answer)
