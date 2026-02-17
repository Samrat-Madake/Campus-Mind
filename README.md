📘 Trustworthy Educational RAG Chatbot

A Retrieval-Augmented Generation (RAG) based educational chatbot that answers strictly from institute-approved material with confidence-aware decision logic and human-in-the-loop verification.

## Project Overview

Large Language Models are powerful — but in educational institutions, accuracy and trust matter more than creativity.
This project implements a retrieval-first, confidence-aware AI assistant that:
Answers only from faculty-uploaded study material
Computes a semantic confidence score before generating responses
Escalates low-confidence questions to mentors
Publishes faculty-verified answers separately
Maintains audit logs for traceability
This is not just a chatbot wrapper — it is a controlled AI system designed for academic reliability.


🏗️ System Architecture

The system follows a two-stage RAG architecture:

1️⃣ Ingestion Stage (Offline)

Faculty uploads PDFs (study material)

Documents are:
Loaded
Cleaned
Split into semantic chunks
Chunks are converted into embeddings (BGE model)
Embeddings are stored in FAISS vector database
PDF → Chunking → Embeddings → Vector Database (FAISS)

2️⃣ Inference Stage (Runtime)

Student submits question

Query is embedded
Similarity search retrieves top-K chunks
Confidence score is computed
If confidence is:
✅ High → LLM generates grounded answer
❌ Low → Escalated to mentor
Mentor answers are stored and published as verified knowledge

Query → Embedding → FAISS → Confidence → LLM / Mentor

🧠 Core Design Principles
🔒 1. Retrieval-First

LLM never answers from its own memory.
It only answers using retrieved institute content.

📊 2. Confidence-Aware Generation

Confidence is computed using semantic similarity scores:
confidence = average(top_k_similarity_scores)
If confidence < threshold:
No answer is generated
Query is escalated to mentor
This prevents hallucination.

👨‍🏫 3. Human-in-the-Loop

Low-confidence queries are:
Added to mentor queue
Answered by faculty
Published in "Verified Answers" section
AI assists. Humans remain accountable.

💻 Tech Stack
# Backend
FastAPI
Uvicorn
FAISS
LangChain
HuggingFace Embeddings (BAAI/bge-base-en-v1.5)
Groq LLM (LLaMA 3)
JSON-based persistence (MVP)

# Frontend
React (Vite)
React Markdown
LocalStorage (chat persistence)
Custom CSS UI

📂 Project Structure
backend/
 ├── app/
 │   ├── ingestion/
 │   ├── rag/
 │   ├── routes/
 │   ├── models/
 │   └── main.py
 ├── data/
 │   ├── pdfs/
 │   ├── mentor_queue.json
 │   └── audit_logs.json
 └── requirements.txt

frontend/
 ├── src/
 │   ├── pages/
 │   ├── components/
 │   ├── api/
 │   └── App.jsx



✨ Features

# 🎓 Student Features

Ask syllabus-related questions
Confidence score display
Source transparency
Persistent chat history (localStorage)
Escalation notification

🛡️ Mentor Features
View pending low-confidence questions
Submit verified answers
Answered questions move to verified section

📘 Verified Knowledge
Dedicated page for faculty-verified answers
Read-only trusted academic responses

📝 Audit Logging
Every query logs:
Question
Confidence
Action (answered/escalated)
Sources
Timestamp
Ensures full traceability.



🔧 Installation Guide
1️⃣ Backend Setup
cd backend
python -m venv myenv
source myenv/bin/activate   # Windows: myenv\Scripts\activate
pip install -r requirements.txt


Create .env file:
GROQ_API_KEY=your_key

Run backend:
uvicorn app.main:app --reload


Backend runs at:
http://localhost:8000

2️⃣ Frontend Setup
cd frontend
npm install
npm run dev


Frontend runs at:
http://localhost:5173

🚀 Deployment Strategy
Frontend: Vercel / Netlify
Backend: Docker + EC2 / Railway / Render
Production server: Gunicorn + Uvicorn workers
Environment variables secured via cloud config

### Future Improvements
Hybrid Retrieval (Vector + Keyword)
Multi-query expansion
Cross-encoder re-ranking
Database-backed persistence
Role-based authentication
Instructor upload dashboard
Scaling for 10k+ users




🏁 Final Note

This project is a demonstration of how AI systems can be made trustworthy, explainable, and institution-ready, rather than just intelligent.
