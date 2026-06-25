# utils/ollama_client.py

import requests
import time
from typing import Optional

from utils.config import (
    OLLAMA_URL,
    OLLAMA_MODEL_MATH,
    OLLAMA_MODEL_SUMMARY,
)

DEFAULT_TIMEOUT = 240
MAX_RETRIES = 2
RETRY_DELAY = 2


def _call_ollama(model: str, prompt: str) -> str:
    """
    Robust Ollama caller using /api/chat
    """

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
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

            # Chat API returns: {"message": {"content": "..."}}
            return data.get("message", {}).get("content", "").strip()

        except Exception as e:
            last_error = str(e)

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
                continue

            return f"Ollama error type is: {last_error}"


def ask_ollama_math(prompt: str) -> str:
    return _call_ollama(OLLAMA_MODEL_MATH, prompt)


def ask_ollama_summary(prompt: str) -> str:
    return _call_ollama(OLLAMA_MODEL_SUMMARY, prompt)
