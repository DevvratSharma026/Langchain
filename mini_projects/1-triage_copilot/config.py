import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

MODELS = {
    "groq":"groq:openai/gpt-oss-20b",
    "gemini": "google_genai:gemini-3.5-flash-lite"
}

def get_model():
    load_dotenv(override=True)
    provider = os.getenv("MODEL_PROVIDER", "groq").lower()
    
    if provider not in MODELS:
        valid_option = ", ".join(MODELS.keys())
        raise ValueError(f"Inavalid MODEL_PROVIDER '{provider}'. Valid MODEL_PROVIDER are: {valid_option}")
    return init_chat_model(MODELS[provider])