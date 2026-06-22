# utils/model_router.py

from config import USE_OLLAMA
from utils.ollama_client import ask_ollama_math, ask_ollama_summary

# Optional fallback (only if you still use OpenAI)
try:
    from utils.openai_client import ask_openai
except ImportError:
    ask_openai = None


def ask_model_math(prompt: str) -> str:
    if USE_OLLAMA:
        return ask_ollama_math(prompt)
    if ask_openai:
        return ask_openai(prompt)
    return "No model available."


def ask_model_summary(prompt: str) -> str:
    if USE_OLLAMA:
        return ask_ollama_summary(prompt)
    if ask_openai:
        return ask_openai(prompt)
    return "No model available."

# from config import USE_OLLAMA
# from utils.ollama_client import ask_ollama_math, ask_ollama_summary

# # Optional fallback (only if you still use OpenAI)
# try:
#     from utils.openai_client import ask_openai
# except ImportError:
#     ask_openai = None


# def ask_model_math(prompt: str) -> str:
#     if USE_OLLAMA:
#         return ask_ollama_math(prompt)
#     if ask_openai:
#         return ask_openai(prompt)
#     return "No model available."


# def ask_model_summary(prompt: str) -> str:
#     if USE_OLLAMA:
#         return ask_ollama_summary(prompt)
#     if ask_openai:
#         return ask_openai(prompt)
#     return "No model available."
