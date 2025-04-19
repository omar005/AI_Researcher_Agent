import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
API_KEY = os.getenv("API_KEY")

# LLM Configuration
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  # Add this line

# Available models
AVAILABLE_MODELS = {
    "deepseek-r1-distill-llama-70b": "deepseek-r1-distill-llama-70b",
    "llama3-70b-8192": "llama3-70b-8192",
    "mistral-saba-24b": "mistral-saba-24b",
    "gemma2-9b-it": "gemma2-9b-it"
}

DEFAULT_MODEL = "llama3-70b-8192"

# Flask Configuration
DEBUG = os.getenv("DEBUG", "False") == "True"
PORT = int(os.getenv("PORT", "5000"))
HOST = os.getenv("HOST", "0.0.0.0")
