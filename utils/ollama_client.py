import requests
import json
from utils.config import (
    OLLAMA_URL,
    OLLAMA_MODEL_MATH,
    OLLAMA_MODEL_SUMMARY,
    USE_OLLAMA
)

# ============================================================
# INTERNAL HELPERS
# ============================================================

def _safe_parse_ollama_response(response_text: str):
    """
    Handles:
    - normal JSON
    - streaming JSON (multiple lines)
    - plain text fallback
    """
    text = response_text.strip()

    # 1) Try direct JSON
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            if "message" in data and "content" in data["message"]:
                return data["message"]["content"].strip()
            if "response" in data:
                return data["response"].strip()
    except:
        pass

    # 2) Try streaming JSON (line-by-line)
    for line in text.splitlines():
        try:
            data = json.loads(line)
            if "message" in data and "content" in data["message"]:
                return data["message"]["content"].strip()
            if "response" in data:
                return data["response"].strip()
        except:
            continue

    # 3) Fallback: return raw text
    return text


# ============================================================
# LOW-LEVEL CALLS
# ============================================================

def _call_chat(model: str, prompt: str) -> str:
    """
    Uses /api/chat (multi-turn chat style)
    """
    if not USE_OLLAMA:
        return "Ollama disabled in config.py"

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    try:
        print("\n================ OLLAMA CHAT DEBUG ================")
        print(f"URL: {OLLAMA_URL}/api/chat")
        print(f"MODEL: {model}")
        print(f"PROMPT: {prompt[:200]}...")
        print("Sending request...")

        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json=payload,
            timeout=30
        )

        print(f"STATUS CODE: {response.status_code}")
        response.raise_for_status()

        raw = response.text
        print("RAW CHAT RESPONSE:", raw[:500])

        return _safe_parse_ollama_response(raw)

    except Exception as e:
        return f"Chat Error: {str(e)}"


def _call_generate(model: str, prompt: str) -> str:
    """
    Uses /api/generate (single-shot generation)
    """
    if not USE_OLLAMA:
        return "Ollama disabled in config.py"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        print("\n================ OLLAMA GENERATE DEBUG ================")
        print(f"URL: {OLLAMA_URL}/api/generate")
        print(f"MODEL: {model}")
        print(f"PROMPT: {prompt[:200]}...")
        print("Sending request...")

        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=30
        )

        print(f"STATUS CODE: {response.status_code}")
        response.raise_for_status()

        raw = response.text
        print("RAW GENERATE RESPONSE:", raw[:500])

        return _safe_parse_ollama_response(raw)

    except Exception as e:
        return f"Generate Error: {str(e)}"


# ============================================================
# PUBLIC FUNCTIONS (CLEAN API FOR YOUR APP)
# ============================================================

def ask_ollama_math(prompt: str) -> str:
    """
    Math engine → single-shot reasoning → /api/generate
    """
    return _call_generate(OLLAMA_MODEL_MATH, prompt)


def ask_ollama_summary(prompt: str) -> str:
    """
    Summary engine → single-shot → /api/generate
    """
    # Force JSON output for stability
    json_prompt = f"""
Respond ONLY in valid JSON:

{{
  "summary": ""
}}

CHAPTER TEXT:
{prompt}
"""
    return _call_generate(OLLAMA_MODEL_SUMMARY, json_prompt)


def ask_ollama_chat(prompt: str) -> str:
    """
    AI Tutor → multi-turn → /api/chat
    """
    return _call_chat(OLLAMA_MODEL_MATH, prompt)
