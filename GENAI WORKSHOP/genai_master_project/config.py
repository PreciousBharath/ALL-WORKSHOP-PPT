"""
GenAI Master Project - Configuration Management
"""
import os

APP_TITLE = "Generative AI Master Suite"
VERSION = "2.0.0"

# Fallback / Mock Settings
DEFAULT_EMBEDDING_DIM = 64
SAMPLE_DOCS_DIR = os.path.join(os.path.dirname(__file__), "data", "sample_docs")

# API Keys (Loaded from environment or Streamlit UI inputs)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
