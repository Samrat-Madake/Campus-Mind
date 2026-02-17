import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# RAG Settings
# CONFIDENCE_THRESHOLD = 0.6
CONFIDENCE_THRESHOLD = 0.55
TOP_K = 4