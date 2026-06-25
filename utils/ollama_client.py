import requests
from utils.config import OLLAMA_URL, OLLAMA_MODEL_MATH, OLLAMA_MODEL_SUMMARY


def _call_ollama(model: str, prompt: str) -> str:
    """
    Calls Ollama using the /api/generate endpoint.
    Returns a clean string response.
    """

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
        resp.raise_for_status()

        data = resp.json()
        return (data.get("response") or "").strip()

    except Exception as e:
        return f"Ollama error: {str(e)}"


def ask_ollama_math(prompt: str) -> str:
    return _call_ollama(OLLAMA_MODEL_MATH, prompt)


def ask_ollama_summary(prompt: str) -> str:
    return _call_ollama(OLLAMA_MODEL_SUMMARY, prompt)
