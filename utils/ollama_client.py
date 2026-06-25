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


def _debug(msg: str):
    print(f"[OLLAMA DEBUG] {msg}")


def _call_ollama(model: str, prompt: str)->str:
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    _debug(f"Calling Ollama URL: {OLLAMA_URL}")
    _debug(f"Model: {model}")
    _debug(f"Payload: {payload}")

    last_error: Optional[str] = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            _debug(f"Attempt {attempt}/{MAX_RETRIES}")

            resp = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=DEFAULT_TIMEOUT,
            )

            _debug(f"HTTP Status: {resp.status_code}")
            _debug(f"Raw Response: {resp.text}")

            resp.raise_for_status()

            data = resp.json()
            content = data.get("message", {}).get("content", "").strip()

            _debug(f"Parsed Content: {content}")

            return content

        except Exception as e:
            last_error = str(e)
            _debug(f"Error: {last_error}")

            if attempt < MAX_RETRIES:
                _debug(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
                continue

            return f"Ollama error: {last_error}"


def ask_ollama_math(prompt: str) -> str:
    _debug("ask_ollama_math called")
    return _call_ollama(OLLAMA_MODEL_MATH, prompt)


def ask_ollama_summary(prompt: str) -> str:
    _debug("ask_ollama_summary called")
    return _call_ollama(OLLAMA_MODEL_SUMMARY, prompt)