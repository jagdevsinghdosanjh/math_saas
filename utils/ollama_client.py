# utils/ollama_client.py

import requests
from utils.config import (
    OLLAMA_URL,
    OLLAMA_MODEL_MATH,
    OLLAMA_MODEL_SUMMARY,
)

# Cloudflare timeout limit is ~100 seconds → keep below that
DEFAULT_TIMEOUT = 90


def _call_ollama(model: str, prompt: str) -> str:
    """
    Low-level Ollama caller.
    Handles:
    - Timeout protection
    - HTTP errors
    - Missing response fields
    """

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    try:
        resp = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=DEFAULT_TIMEOUT
        )
        resp.raise_for_status()

        data = resp.json()
        return (data.get("response") or "").strip()

    except Exception as e:
        # Always return a string (router + services expect this)
        return f"Ollama error: {str(e)}"


def ask_ollama_math(prompt: str) -> str:
    """Call the math/logic model (deepseek-r1)."""
    return _call_ollama(OLLAMA_MODEL_MATH, prompt)


def ask_ollama_summary(prompt: str) -> str:
    """Call the fast text model (llama3)."""
    return _call_ollama(OLLAMA_MODEL_SUMMARY, prompt)
