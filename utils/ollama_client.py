# utils/ollama_client.py

import requests
import time
from typing import Optional

from utils.config import (
    OLLAMA_URL,
    OLLAMA_MODEL_MATH,
    OLLAMA_MODEL_SUMMARY,
)

# Cloudflare can drop long requests → keep timeout high
DEFAULT_TIMEOUT = 240

# Retry settings
MAX_RETRIES = 2
RETRY_DELAY = 2  # seconds


def _call_ollama(model: str, prompt: str) -> str:
    """
    Robust Ollama caller with:
    - Retry logic
    - Cloudflare-safe timeouts
    - Graceful fallback
    - Clean error messages
    """

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    last_error: Optional[str] = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=DEFAULT_TIMEOUT,
            )
            resp.raise_for_status()

            data = resp.json()
            return (data.get("response") or "").strip()

        except Exception as e:
            last_error = str(e)

            # Retry only if attempts remain
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
                continue

    # Final fallback error
    return f"Ollama error: {last_error}"


def ask_ollama_math(prompt: str) -> str:
    """Call the math/logic model."""
    return _call_ollama(OLLAMA_MODEL_MATH, prompt)


def ask_ollama_summary(prompt: str) -> str:
    """Call the fast text model."""
    return _call_ollama(OLLAMA_MODEL_SUMMARY, prompt)