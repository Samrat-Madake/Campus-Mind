from app.rag.retriever import get_relevant_chunks_with_scores
from app.rag.generator import generate_answer
from app.rag.confidence import compute_confidence

# question = "What is exploratory data analysis?"
question = "What is Importance of the Curse of Dimensionality?"

results = get_relevant_chunks_with_scores(question)
docs = [doc for doc, _ in results]
confidence = compute_confidence(results)

print("Confidence:", confidence)

if confidence < 0.6:
    print("Escalate to mentor")
else:
    answer = generate_answer(docs, question)
    print(answer)
