# utils/model_router.py

from utils.ollama_client import ask_ollama_math, ask_ollama_chat


def ask_model(prompt: str, task: str = "math") -> str:
    """
    Router only used for AI Tutor now.
    Math, summary, questions bypass router.
    """

    if task == "tutor":
        return ask_ollama_chat(prompt)

    # Default: math engine
    return ask_ollama_math(prompt)
