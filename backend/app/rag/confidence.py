import numpy as np


def compute_confidence(scored_docs):
    """
    Computes confidence from FAISS distance scores.
    Lower distance = higher confidence.

    Tuned for:
    - sentence-transformers/all-MiniLM-L6-v2
    - FAISS
    """

    if not scored_docs:
        return 0.0

    # Extract FAISS distances (already floats)
    scores = [float(score) for _, score in scored_docs]

    avg_score = sum(scores) / len(scores)

    # --- Distance → confidence mapping ---
    # Good matches:     0.2 – 0.6
    # Partial matches:  0.6 – 1.0
    # Weak matches:     > 1.0

    if avg_score <= 0.6:
        confidence = 0.85
    elif avg_score <= 0.8:
        confidence = 0.65
    elif avg_score <= 1.0:
        confidence = 0.45
    else:
        confidence = 0.15

    return float(confidence)
