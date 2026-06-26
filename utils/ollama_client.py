# utils/ollama_client.py

import requests
import json
from utils.config import (
    OLLAMA_URL,
    OLLAMA_MODEL_MATH,
    OLLAMA_MODEL_MATH_HEAVY,
    OLLAMA_MODEL_SUMMARY,
    OLLAMA_MODEL_QUESTIONS,
)

TIMEOUT = 90
RETRIES = 2


# ============================================================
# SAFE PARSER
# ============================================================

def _safe_parse(text: str) -> str:
    """
    Always returns a string.
    Attempts:
    1. Direct JSON
    2. Streaming JSON
    3. Raw text fallback
    """

    cleaned = text.strip()

    # Try direct JSON
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict):
            if "message" in data and "content" in data["message"]:
                return str(data["message"]["content"]).strip()
            if "response" in data:
                return str(data["response"]).strip()
    except json.JSONDecodeError:
        pass

    # Try streaming JSON
    for line in cleaned.splitlines():
        try:
            data = json.loads(line)
            if "message" in data and "content" in data["message"]:
                return str(data["message"]["content"]).strip()
            if "response" in data:
                return str(data["response"]).strip()
        except json.JSONDecodeError:
            continue

    # Fallback: return raw text
    return cleaned


# ============================================================
# HTTP POST WRAPPER (ALWAYS RETURNS str)
# ============================================================

def _post(url: str, payload: dict) -> str:
    """
    Sends POST request with retry logic.
    ALWAYS returns a string (never None).
    """

    for attempt in range(RETRIES):
        try:
            response = requests.post(url, json=payload, timeout=TIMEOUT)
            response.raise_for_status()
            return _safe_parse(response.text)

        except requests.exceptions.Timeout:
            if attempt == RETRIES - 1:
                return "Error: Model timed out."

        except Exception as e:
            if attempt == RETRIES - 1:
                return f"Error: {str(e)}"

    # Should never reach here, but return string anyway
    return "Error: Unknown failure."


# ============================================================
# PUBLIC FUNCTIONS (ALWAYS RETURN str)
# ============================================================

def ask_ollama_math(prompt: str) -> str:
    return _post(
        f"{OLLAMA_URL}/api/generate",
        {"model": OLLAMA_MODEL_MATH, "prompt": prompt, "stream": False},
    )

def ask_ollama_math_heavy(prompt: str) -> str:
        return _post(
        f"{OLLAMA_URL}/api/generate",
        {"model": OLLAMA_MODEL_MATH_HEAVY, "prompt": prompt, "stream": False},
    )


def ask_ollama_summary(prompt: str) -> str:
    json_prompt = f"""
Respond ONLY in valid JSON:

{{
  "summary": ""
}}

CHAPTER TEXT:
{prompt}
"""
    return _post(
        f"{OLLAMA_URL}/api/generate",
        {"model": OLLAMA_MODEL_SUMMARY, "prompt": json_prompt, "stream": False},
    )


def ask_ollama_questions(prompt: str) -> str:
    return _post(
        f"{OLLAMA_URL}/api/generate",
        {"model": OLLAMA_MODEL_QUESTIONS, "prompt": prompt, "stream": False},
    )


def ask_ollama_chat(prompt: str) -> str:
    return _post(
        f"{OLLAMA_URL}/api/chat",
        {
            "model": OLLAMA_MODEL_MATH,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        },
    )
